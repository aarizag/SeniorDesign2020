from gensim.models import KeyedVectors
import time
import numpy as np
import gzip
import os

model_folder = '/Users/arizaga/Documents/School/SeniorDesign/word2vecDemo/models/'
dict_folder = '/Users/arizaga/Documents/School/SeniorDesign/word2vecDemo/dictionaries/'
model_filename = 'GoogleNews-vectors-negative300.bin.gz'
slim_filename = 'GoogleNews-vectors-negative300-SLIM.bin.gz'

max_suffix_len = 2
min_base_len = 8

words = set()
for dict_filename in os.listdir(dict_folder):
    with gzip.open(dict_folder + dict_filename, 'rt', encoding='utf8') as f:
        temp = f.readlines()
        save_len = len(temp)
        for i in range(len(temp)):
            temp[i] = temp[i].strip().lower()
        temp = set(temp)
        print('%s: %d -> %d' % (dict_filename, save_len, len(temp)))
    words |= temp
print('combined: %d' % (len(words)))

start = time.time()

# Load Google's pre-trained Word2Vec model.
model = KeyedVectors.load_word2vec_format('../sample_text/GoogleNews-vectors-negative300.bin.gz', binary=True)

print(f'Finished loading original model {round((time.time()-start)/60, 2)} min')
print(f'word2vec: {len(model.vocab)}')
print(f'non-phrases: {len([w for w in model.vocab.keys() if "_" not in w])}')

indices_to_delete = []
j = 0
suffix_grace_words = 0
for i, w in enumerate(model.index2word):
    l = w.strip().lower()
    found = l in words
    if not found:
        for s in range(1, 1+max_suffix_len):
            if len(l)-s<min_base_len:
                break
            elif l[:-s] in words:
                suffix_grace_words += 1
                found = True
                break

    if found:
        model.vocab[w].index = j
        j += 1
    else:
        del model.vocab[w]
        indices_to_delete.append(i)

model.syn0 = np.delete(model.syn0, indices_to_delete, axis=0)
print(f'slim: {len(model.vocab)}')
print(f'suffix grace words: {suffix_grace_words}')

model.save_word2vec_format(model_folder + '/' + slim_filename, binary=True)
del model
print(f'slim: {len(model.vocab)}')
# model.save('/Users/arizaga/Documents/School/SeniorDesign/word2vecDemo/models/Google_SLIM.model')


model.save_word2vec_format(model_folder + slim_filename, binary=True)
