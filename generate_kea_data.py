import argparse
import pickle

import os
import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='KEA data generator for Dracoon challenge, hackaburg2018')
    parser.add_argument('-c', '--cache_file', type=str, default='id_to_text.pkl', help='Cache file')
    parser.add_argument('-k', '--kea_data', type=str, default='kea_data', help='KEA data folder')

    args = parser.parse_args()
    text_cache = pickle.load(open(args.cache_file, 'rb'))
    labelled_data = pickle.load(open('download_meta.pickle', 'rb'))

    for node_id, filename, golden_tags in tqdm.tqdm(labelled_data):
        text = text_cache[node_id] or ''

        with open(os.path.join(args.kea_data, filename + ".txt"), 'w') as ff:
            ff.write(text)

        with open(os.path.join(args.kea_data, filename + ".key"), 'w') as ff:
            ff.write('\n'.join(golden_tags))
