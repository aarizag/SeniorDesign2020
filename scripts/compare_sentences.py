from gensim.models import KeyedVectors

from typing import Dict


similarity_model = KeyedVectors.load_word2vec_format('/Users/arizaga/Documents/School/SeniorDesign/word2vecDemo/models/GoogleNews-vectors-negative300-SLIM.bin.gz', binary=True)


def get_similar_from_sentence(sentence: str) -> Dict[str, float]:
    words = sentence.split(' ')
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


class Sentence:
    def __init__(self, sentence, get_similar=False):
        self.sentence = sentence
        self.similar_set = get_similar_from_sentence(sentence) if get_similar and sentence else None

    def compare_to(self, other):
        if self.similar_set is None:
            self.similar_set = get_similar_from_sentence(self.sentence)

        if type(other) == str:
            words = str.split(' ')
        else:
            words = other.sentence.split(' ')

        return sum([self.word_val(word) for word in words]) / len(words)

    def word_val(self, word):
        if self.similar_set is None or word not in self.similar_set:
            return 0
        return self.similar_set[word]

