##
## Normalizing Data
## Jesse Rodriguez Avila
## Senior Design Project

#### reading data using pandas, converting data into array and lowercaseing data ####

import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from xlrd import open_workbook
import gensim
import numpy as np


book = open_workbook('./ignore/UNSPSC English v220601 project.xlsx')
dict_list = []
sheet = book.sheet_by_index(0)
# read header values into the list
keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

for row_index in range(1, sheet.nrows):
    d = {keys[col_index]: sheet.cell(row_index, col_index).value
         for col_index in range(sheet.ncols)}
    dict_list.append(d)
listOfEntry = []

for entry in dict_list:
    a = entry.get("Segment Title")
    c = entry.get("Family Title")
    e = entry.get("Class Title")
    g = entry.get("Commodity Title")
    i = entry.get("Commodity")
    result = str(a) + " " + str(c)+" "+str(e) + " " + str(g)
    sen = sent_tokenize(result.lower())
    listOfEntry.append(sen)
    e, f, g, h = "", "", "", ""


print(len(listOfEntry))

import re
def punctuation_remove(tokenized_words):
    #tokeinzed means converting a sentence into an array of words.
    #every word in the array will then become a token
    punctuation_removed = []
    
    for i in range(len(tokenized_words)):
        #remove all punctuations from Token at index i
        new_word_without_punct = re.sub(r'[^\w\s]', '', tokenized_words[i])
        
        # if the word is not blank append to new array
        if new_word_without_punct != '':
            punctuation_removed.append(new_word_without_punct)
            
    return punctuation_removed


# -- Remove Stop words ---------------
from nltk.corpus import stopwords
def stopwords_remove(tokenized_words):
    #array with stopwords removed
    stopwords_removed = []

    # remove stop words from tokenized sentence
    stopwords_englishLanguage = set(stopwords.words('english'))
    
    for i in range(len(tokenized_words)):
        if tokenized_words[i] not in stopwords_englishLanguage:
            stopwords_removed.append(tokenized_words[i])
    
    return stopwords_removed


# -- lematization ---------------
from nltk.stem import WordNetLemmatizer 
def lematization(tokenized_words):
    # convert list of tokenized words into normalized form
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for i in range(len(tokenized_words)):
        lemma = lemmatizer.lemmatize(tokenized_words[i], pos='v')
        lemmas.append(lemma)
    return lemmas

# final Part: normalizing_data
def normalizing_data(tokenized_words):
    normalized = lematization(stopwords_remove(punctuation_remove(tokenized_words)))
    return normalized
file_docs=[]
for input in listOfEntry:
    for j in input:
        token = sent_tokenize(j)
        for a in token:
            tokens = word_tokenize(a)
            tokens = normalizing_data(tokens)
    #print(tokens)
    file_docs.append(tokens)

print(len(file_docs))

dictionary = gensim.corpora.Dictionary(file_docs)
corpus = [dictionary.doc2bow(entry, allow_update=True) for entry in file_docs]
tf_idf = gensim.models.TfidfModel(corpus,dictionary)
for doc in tf_idf[corpus]:
    print([[dictionary[id], freq] for id, freq in doc])



