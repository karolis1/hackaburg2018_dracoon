import argparse
import pickle
import os
import tqdm

from download_files import download_all
from preprocessing.text_extraction import extract_text
from selectkeywords import selectkeywords

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tag generator for Dracoon challenge, hackaburg2018')
    parser.add_argument('-r', '--redownload', type=bool, default=True, help='Redownload missing files')
    parser.add_argument('-d', '--data_folder', type=str, default='data', help='Data file folder',)
    parser.add_argument('-f', '--results_file', type=str, default='predicted_tags', help='Predicted tags')
    parser.add_argument('-m', '--method', type=str, choices=['rake', 'gensim', 'keras'],
                        help='Keyword extraction method')
    parser.add_argument('-u', '--use_cache', type=bool, default=True, help='Use cache?')
    parser.add_argument('-c', '--cache_file', type=str, default='id_to_text.pkl', help='Cache file')



    args = parser.parse_args()

    if args.use_cache:
        text_cache = pickle.load(open(args.cache_file, 'rb'))
    if args.redownload:
        download_all()

    labelled_data = pickle.load(open('download_meta.pickle', 'rb'))

    broken_files = 0
    broken_file_list = []

    for node_id, filename, golden_tags in tqdm.tqdm(labelled_data):
        if args.use_cache:
            text = text_cache[node_id] or ''
        else:
            try:
                text = extract_text(os.path.join(args.data_folder, filename))
            except:
                text = ''
                print("WARNING: {} failed to parse text".format(filename))
                broken_file_list.append(filename)

        predicted_tags = selectkeywords(text)

        print("GOLD:")
        print(golden_tags)
        print("PREDICTED:")
        print(predicted_tags[:15])
        print("\n---\n")

    if args.results_file:
        pass