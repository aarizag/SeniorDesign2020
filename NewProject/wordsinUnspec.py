import nltk,re,pprint
import os
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim
from xlrd import open_workbook
from nltk.corpus import stopwords
import operator

book = open_workbook('UNSPSC English v220601 project.xlsx')
'''book = open_workbook('Unspec List.xlsx')'''
'''To work on the UNSPSC sheet you need to change the values of 0 to 12 and 1 to
16 in order to make the it work.'''
dict_list = []
sheet = book.sheet_by_index(0)
# read header values into the list
keys = [sheet.cell(12, col_index).value for col_index in range(sheet.ncols)]

for row_index in range(13, sheet.nrows):
    d = {keys[col_index]: sheet.cell(row_index, col_index).value
         for col_index in range(sheet.ncols)}
    dict_list.append(d)

listOfEntry = []
tokenSen = []
sen = []
keyvaluePair = []
counter = 0

for entry in dict_list:
    e = entry.get("Class Title")
    f = entry.get("Class Definition")
    g = entry.get("Commodity Title")
    h = entry.get("Commodity Definition")
    i = entry.get("Commodity")
    if(f != "" and h != ""):
        result = e+". "+f+". "+g+". "+h+". "
    elif(f != "" and h == ""):
        result = e+". "+f+". "+g+". "+h
    elif(f == "" and h != ""):
        result = e+". "+f+" "+g+". "+h+". "
    else:
        result = e + ". " + f + "" + g + ". " + h
    sen = sent_tokenize(result.lower())
    listOfEntry.append(sen)
    keyvaluePair.append(i)
    e, f, g, h = "", "", "", ""



stop_words = set(stopwords.words('english'))
file_docs = []


for input in listOfEntry:
    for j in input:
        tokens = word_tokenize(j)
        tokens = [w for w in tokens if not w in stop_words]
    file_docs.append(tokens)

print("Number of documents:", len(file_docs))

"""
Dictionary is a mapping between normalized words and their integer IDs
Token2id is a type of dict of(str, int).
id2token is the same but is a lazy manner to save on memory.
To get the total amount of corpus positions which is the number
of processed words.
"""
dictionary = gensim.corpora.Dictionary(file_docs)
"""
In the coming function call we will be converting a document to a beg of words
the tuple created is the token Id of the word and the token count for that word

"""


corpus = [dictionary.doc2bow(entry) for entry in file_docs]


tf_idf = gensim.models.TfidfModel(corpus)


sims = gensim.similarities.Similarity('dir', tf_idf[corpus], num_features=len(dictionary))


test = "MASS TRANSPORTATION - RAIL VEHICLE PARTS AND ACCESSORIES"
test = test.lower()

query_doc = word_tokenize(test)
print(query_doc)
query_doc_bow = dictionary.doc2bow(query_doc, True)
print(query_doc_bow)

query_doc_tf_idf = tf_idf[query_doc_bow]



listnew =[]
listnew = list(zip(keyvaluePair,sims[query_doc_tf_idf]))

listnew.sort(key = operator.itemgetter(1),reverse = True)

for i in range(5):
    print(listnew[i])


""" a = entry.get("Segment Title")
a.replace('.'," ")
b = entry.get("Segment Definition")
b.replace('.'," ")
c = entry.get("Family Title")
c.replace('.'," ")
d =entry.get("Family Definition")
d.replace('.'," ")  """
