from gensim.models import KeyedVectors

from typing import Dict


similarity_model = KeyedVectors.load_word2vec_format('/Users/arizaga/Documents/School/SeniorDesign/word2vecDemo/models/GoogleNews-vectors-negative300-SLIM.bin.gz', binary=True)


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


def deep_compare(base, comparer):
    """
    Do a comparison by comparing each word in the base to every other word in the comparer sentence and taking an
        average of that total
    :param base: The base sentence being compared to
    :param comparer: The sentence being compared to the base
    :return: a float value representing the similarity between the 2 sentences
    """
    base_words = base.split(' ')
    compared_words = comparer.split(' ')

    total_sums = 0
    for b_word in base_words:
        total_sums += max([similarity_model.similarity(b_word, c_word) for c_word in compared_words])

    return total_sums / len(base_words)
