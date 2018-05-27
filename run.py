import argparse
import pickle
import os
import tqdm

from download_files import download_all
from evaluate_measure import aligned_tag_score
from preprocessing.text_extraction import extract_text, preprocess_text
from selectkeywords import selectkeywords
from gensim.summarization import keywords
from postprocess_tags import postprocess_tags
import word2vec_keywords
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tag generator for Dracoon challenge, hackaburg2018')
    parser.add_argument('-r', '--redownload', type=bool, default=True, help='Redownload missing files')
    parser.add_argument('-d', '--data_folder', type=str, default='data', help='Data file folder',)
    parser.add_argument('-f', '--results_file', type=str, default='predicted_tags', help='Predicted tags')
    parser.add_argument('-m', '--method', type=str, required=True, choices=['rake', 'gensim', 'keras', 'word2vec'],
                        help='Keyword extraction method')
    parser.add_argument('-u', '--use_cache', type=bool, default=True, help='Use cache?')
    parser.add_argument('-c', '--cache_file', type=str, default='id_to_text.pkl', help='Cache file')
    parser.add_argument('-p', '--use_preprocessing', type=bool, default=True, help='Use text preprocessing?')
    parser.add_argument('-pp', '--use_postprocessing', type=bool, default=True, help='Postprocess tags')
    args = parser.parse_args()

    print('Using method:', args.method)

    if args.use_cache:
        text_cache = pickle.load(open(args.cache_file, 'rb'))
    if args.redownload:
        download_all()

    labelled_data = pickle.load(open('download_meta.pickle', 'rb'))

    broken_files = 0
    broken_file_list = []

    doc_scores = []

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

        if args.use_preprocessing:
            text = preprocess_text(text)

        if args.method == 'rake':
            predicted_tags = selectkeywords(text)
        elif args.method == 'gensim':
            predicted_tags = keywords(text).split('\n')
        elif args.method == 'word2vec':
            predicted_tags = word2vec_keywords.extract_keywords(text)

        if args.use_postprocessing:
            predicted_tags = postprocess_tags(predicted_tags)

        doc_scores.append(aligned_tag_score(predicted_tags[:15], golden_tags))

        print("GOLD:")
        print(golden_tags)
        print("PREDICTED:")
        print(predicted_tags[:15])
        print("QUALITY: {}".format(doc_scores[-1]))
        print("\n---\n")


    eval_metric = np.average(doc_scores)

    print("Final EVAL score: {}".format(eval_metric))



    if args.results_file:
        pass
