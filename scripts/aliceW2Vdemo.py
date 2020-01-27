# Python program to generate word vectors using Word2Vec

# importing all necessary modules
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
from gensim.models import Word2Vec

warnings.filterwarnings(action='ignore')


# Reads ‘alice.txt’ file
file_path = "/Users/arizaga/Documents/School/SeniorDesign/word2vecDemo/sample_text/alice.txt"
sample = open(file_path, "r")
s = sample.read()

# Replaces escape character with space
f = s.replace("\n", " ")

data = []

# iterate through each sentence in the file
for i in sent_tokenize(f):
    temp = []

    # tokenize the sentence into words
    for j in word_tokenize(i):
        temp.append(j.lower())

    data.append(temp)

# Create CBOW model
model1 = Word2Vec(data, min_count=1, size=100, window=5)
model1.save('../models/alice_CBOW.model')

# Print results
print("Cosine similarity between 'alice' " +
      "and 'wonderland' - CBOW : ",
      model1.similarity('alice', 'wonderland'))

print("Cosine similarity between 'alice' " +
      "and 'machines' - CBOW : ",
      model1.similarity('alice', 'machines'))

# Create Skip Gram model
model2 = Word2Vec(data, min_count=1, size=100, window=5, sg=1)
model1.save('/Users/arizaga/Documents/School/SeniorDesign/word2vecDemo/models/alice_SG.model')

# Print results
print("Cosine similarity between 'alice' " +
      "and 'wonderland' - Skip Gram : ",
      model2.similarity('alice', 'wonderland'))

print("Cosine similarity between 'alice' " +
      "and 'machines' - Skip Gram : ",
      model2.similarity('alice', 'machines'))
