import nltk
import os
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim
from xlrd import open_workbook
from nltk.corpus import stopwords
import operator
import time
import xlsxwriter
import utils.Normalize


if not os.path.exists('../ignore'):
    os.makedirs('../ignore')

start2=time.time()

book = open_workbook('../sample_text/NormalizedUNSPSC.xlsx')
#book = open_workbook('../ignore/Unspec List2b.xlsx')
'''To work on the UNSPSC sheet you need to change the values of 0 to 12 and 1 to
16 in order to make the it work.'''
dict_list = []
sheet = book.sheet_by_index(0)
# read header values into the list
keys = [sheet.cell(12, col_index).value for col_index in range(sheet.ncols)]

for row_index in range(1, sheet.nrows):
    d = {keys[col_index]: sheet.cell(row_index, col_index).value
         for col_index in range(sheet.ncols)}
    dict_list.append(d)


book = open_workbook('../sample_text/NormalizedEcomm.xlsx')
#book = open_workbook('../ignore/County_List.xlsx')
county_list = []

sheet = book.sheet_by_index(0)
# read header values into the list
keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

for row_index in range(1, sheet.nrows):
    d = {keys[col_index]: sheet.cell(row_index, col_index).value
         for col_index in range(sheet.ncols)}
    #Uncomment these for real use
    county_list.append(d)
    
print(f'Reading excel files done in: {time.time() - start2}')
listOfEntry = []
tokenSen = []
sen = []
keyvaluePair = []
counter = 0

for entry in dict_list:
    a = entry.get("segment title")
    b = entry.get("segment definition")
    c = entry.get("family title")
    d =entry.get("family definition")
    e = entry.get("class title")
    f = entry.get("class definition")
    g = entry.get("commodity ditle")
    h = entry.get("commodity definition")
    i = entry.get("commodity")
    result = str(a)+" "+str(b)+" "+str(c)+" "+str(d)+str(e)+" " + str(f) + " " + str(g)+" "+str(h)
    sen = sent_tokenize(result.lower())
    listOfEntry.append(sen)
    keyvaluePair.append(i)
    e, f, g, h = "", "", "", ""


print(f'Taking family and under in {time.time() - start2}')
stop_words = set(stopwords.words('english'))
file_docs = []
tokens=[]

for input in listOfEntry:
    for j in input:
        token = sent_tokenize(j)
        for a in token:
            tokens = word_tokenize(a)
            tokens = [w for w in tokens if not w in stop_words]
            tokens = [word for word in tokens if word.isalnum()]
    file_docs.append(tokens)

print(f'Tokenize done in {time.time() - start2}')
print("Number of documents:", len(file_docs))

"""
Dictionary is a mapping between normalized words and their integer IDs
Token2id is a type of dict of(str, int).
id2token is the same but is a lazy manner to save on memory.
To get the total amount of corpus positions which is the number
of processed words.
"""
dictionary = gensim.corpora.Dictionary(file_docs)

print(f'Dictionary done in {time.time() - start2}')
"""
In the coming function call we will be converting a document to a beg of words
the tuple created is the token Id of the word and the token count for that word

"""


corpus = [dictionary.doc2bow(entry) for entry in file_docs]


tf_idf = gensim.models.TfidfModel(corpus)


sims = gensim.similarities.Similarity('../ignore/dir', tf_idf[corpus], num_features=len(dictionary))

print(f'Done with building Similarity in {time.time() - start2}')

def NarrowingDown(sheet,county):
    query_doc = word_tokenize(county.lower())
    query_doc = [w for w in query_doc if not w in stop_words]
    query_doc = [word for word in query_doc if word.isalnum()]
    query_doc_bow = dictionary.doc2bow(query_doc, True)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    listnew =[]
    listnew = list(zip(keyvaluePair,sims[query_doc_tf_idf]))
    listNew=[]
    for a in listnew:
        if(a[0]==''):
            continue
        elif(a[1]>0.05):
            listNew.append(a[0])
    excelSheet=workbook.add_worksheet(str(sheet))
    excelSheet.write(0,0,"commodity title")
    excelSheet.write(0,1,"commodity")
    cot = 1
    counter = 0
    for entry in dict_list:
        if(counter < len(listNew)):
            if(entry.get("commodity")==listNew[counter]):
                if(entry.get("commodity title")==""):
                    excelSheet.write(cot,0,"nothing")
                else:
                    excelSheet.write(cot,0,entry.get("commodity title"))
                excelSheet.write(cot,1,entry.get("commodity"))
                cot += 1
                counter += 1
    


workbook = xlsxwriter.Workbook('../sample_text/narrowedSheets.xlsx')
for w in county_list:
    NarrowingDown(int(w.get('COMM_CLS')),str(w.get('KEYWD')))
workbook.close()       
print(f'Narrowing done in {time.time() - start2}')



