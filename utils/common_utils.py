import pickle
from joblib import Memory
memory = Memory("./cache", verbose=0)
import numpy as np
from nltk.corpus import wordnet as wn

try:
    from utils.edit_distance import levenshtein
except:
    from edit_distance import levenshtein


def find_closes_match(token):
    special_characters = '!@#$%^&()-+=.:?/;][{}|\~`1234567890'
    words_chklst = [w for w in wn.words(lang='eng') if
                    len([w for w in list(token) if w in list(w)]) > 0 and not any(
                        c in special_characters for c in w)]
    temp = [(levenshtein(token, w), w) for w in words_chklst]
    return sorted(temp, key=lambda val: val[0])

# caching the function output for quick reruns
@memory.cache
def reduce_result_list(token_distance: list, top_n: int = 20):
    # assumes that the token_distance list of tuples is sorted with distance
    d_nth = token_distance[top_n-1][0]
    top_n_words = [word[1] for word in token_distance if word[0] <= d_nth]
    return np.array(top_n_words)


def return_n_closest_word(token, top_n: int):
    return reduce_result_list(find_closes_match(token), top_n)


def return_top_1_5_10_words(da):
    token, correct_spelling = da[0], da[1]
    result = {
        'incorrect': token,
        'correct': correct_spelling
    }
    token_distance = find_closes_match(token)
    for n in [1, 5, 10]:
        result[n] = list(reduce_result_list(token_distance, top_n=n))

    print(f'Analysis done for {token} !')
    return result


def return_success_at_k(result_list):
    dict_ = result_list[0]
    ks = [k for k in dict_.keys() if k not in ['incorrect', 'correct']]
    success = [[] for _ in ks]
    for d in result_list:
        crr = d['correct']
        for idx, k in enumerate(ks):
            if crr in d[k]:
                success[idx].append(1)
            else:
                success[idx].append(0)

    success_dict = {}
    for k, success_ in zip(ks, success):
        success_dict[k] = success_
    return success_dict
