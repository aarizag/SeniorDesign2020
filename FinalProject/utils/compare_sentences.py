from gensim.models import KeyedVectors

from typing import Dict
import time
from utils.DeepCompare import comparisons


FULL_GOOGLE = '/Users/z12dr/Desktop/Python/models/GoogleNews-vectors-negative300.bin.gz'
SLIM_GOOGLE = '/Users/z12dr/Desktop/Python/models/GoogleNews-vectors-negative300-SLIM.bin.gz'

start = time.time()
similarity_model = KeyedVectors.load_word2vec_format(FULL_GOOGLE, binary=True)
print(f'Model loaded in {time.time() - start}')


def get_most_similar_words(phrase: str) -> Dict[str, float]:
    """
    Get the set of the 10 most similar words for every word in the phrase
    :param phrase: The string being split by white spaces.
    :return: a dictionary with with each key being the word similar to one in the sentence and the value being the
        similarity
    """
    words = phrase.split(' ')
    all_similar = {}
    for word in words:
        if word not in similarity_model.vocab:
            continue
        all_similar[word] = 1.0
        similar = similarity_model.most_similar(word)
        for sim, percent in similar:
            if sim in all_similar:
                all_similar[sim] = max(percent, all_similar[sim])
            else:
                all_similar[sim] = percent

    return all_similar


def shallow_compare(base: str, comparer: str) -> float:
    """
    Perform a shallow comparison between 2 sentences { O(2n) }
        Instead of comparing every word to every other word, get the set of words that are similar to the words in the
        base sentence and only use the values that are present to compare to the comparer sentence
    :param base: The base sentence being compared to
    :param comparer: The sentence being compared to the base
    :return: a float value representing the similarity between the 2 sentences
    """
    def word_val(word, similar_set):
        if similar_set is None or word not in similar_set:
            return 0
        return similar_set[word]

    comp_words = comparer.split(' ')
    base_similar_set = get_most_similar_words(base)

    return sum([word_val(word, base_similar_set) for word in comp_words]) / len(comp_words)


def deep_compare(base: str, comparer: str) -> float:
    """
    Do a comparison by comparing each word in the base to every other word in the comparer sentence and taking an
        average of that total
    :param base: The base sentence being compared to
    :param comparer: The sentence being compared to the base
    :return: a float value representing the similarity between the 2 sentences
    
    base_words = base.split(' ')
    compared_words = comparer.split(' ')

    total_sums = 0
    for b_word in base_words:
        if b_word not in similarity_model.vocab:
            continue

        total_sums += max([similarity_model.similarity(b_word, c_word) if c_word in similarity_model.vocab else 0
                           for c_word in compared_words])

"""
    #this function will return a float of how similar the two strings are
    return comparisons(base,comparer)

