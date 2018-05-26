import re

import numpy as np
import scipy.spatial
from gensim.models import KeyedVectors
import math

# model from https://devmount.github.io/GermanWordEmbeddings/
fname = 'german.model'
german_model = KeyedVectors.load_word2vec_format(fname, binary=True)


def tag_pair_similarity(guess, gold):
    guess_tokens = re.split(r'[^\w]+', guess)
    guess_vecs = [german_model[token] for token in guess_tokens]


    gold_tokens = re.split(r'[^\w]+', gold)
    gold_vecs = [german_model[token] for token in gold_tokens]

    guess_vec = np.average(guess_vecs, axis=0)
    gold_vec = np.average(gold_vecs, axis=0)

    cos_sim = 1 - scipy.spatial.distance.cosine(guess_vec, gold_vec)

    return cos_sim


def closest_to_model(token):
    if token in german_model:
        return token
    elif token.lower() in german_model:
        return token.lower()
    elif token.lower().capitalize() in german_model:
        return token.lower().capitalize()
    else:
        return None


def aligned_tag_score(guess_tags, gold_tags):
    tag_scores = []
    for guess_tag in guess_tags:
        current_tag_score = 0

        guess_tag = closest_to_model(guess_tag)

        if not guess_tag:
            continue
        for gold_tag in gold_tags:
            gold_tag = closest_to_model(gold_tag)
            if not gold_tag:
                continue
            current_tag_score = max(current_tag_score, tag_pair_similarity(guess_tag, gold_tag))
        tag_scores.append(current_tag_score)

    score = np.average(tag_scores)

    if math.isnan(score):
        return 0
    else:
        return score
