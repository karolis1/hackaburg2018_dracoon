import subprocess
import glob
import numpy as np
import os

from evaluate_measure import aligned_tag_score
from postprocess_tags import postprocess_tags

kea_train = '/home/justas/git/hackaburg18/hackaburg2018_dracoon/kea_sets/kea_train'
kea_test_labelled = '/home/justas/git/hackaburg18/hackaburg2018_dracoon/kea_sets/kea_test'
kea_test_unlabelled = '/home/justas/git/hackaburg18/hackaburg2018_dracoon/kea_sets/kea_test_unlabelled'

dir_path = os.path.dirname(os.path.realpath(__file__))


def train_kea():
    print("TRAINING")
    subprocess.run(dir_path + "/kea_train.sh")


def evaluate_kea():
    print("EVALUATE")
    subprocess.call(dir_path + "/kea_eval.sh")


def end_to_end_kea(postprocess=False):
    train_kea()
    evaluate_kea()
    gold_test_tags = glob.glob(kea_test_labelled + '/*.key')
    predicted_test_tags = glob.glob(kea_test_unlabelled + '/*.key')

    doc_scores = []

    for gold_file, predicted_file in zip(gold_test_tags, predicted_test_tags):
        with open(gold_file) as f:
            golden_tags = list(map(lambda x: x.strip(), f.read().split('\n')))

        with open(predicted_file) as f:
            predicted_tags = list(map(lambda x: x.strip(), f.read().split('\n')))
            if postprocess:
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
