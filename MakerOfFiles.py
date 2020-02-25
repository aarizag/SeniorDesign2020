import nltk
import re
from gensim import corpora
from gensim.test.utils import get_tmpfile
from gensim.models import TfidfModel
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
from os import listdir, makedirs
from os.path import isfile, join, exists
import os
from nltk.corpus import stopwords
from xlrd import open_workbook
import operator
import json
import pandas as pd
from gensim.models import LsiModel
from gensim import similarities
import gensim
import numpy as np
from gensim.corpora import MmCorpus
import warnings
import time

warnings.simplefilter('ignore')

start=time.time()

book = open_workbook('ignore/UNSPSC English v220601 project.xlsx')
#book = open_workbook('ignore/Unspec List2b.xlsx')
'''To work on the UNSPSC sheet you need to change the values of 0 to 12 and 1 to
16 in order to make the it work.'''
dict_list = []
sheet = book.sheet_by_index(0)
# read header values into the list
keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

for row_index in range(1, sheet.nrows):
    d = {keys[col_index]: sheet.cell(row_index, col_index).value
         for col_index in range(sheet.ncols)}
    dict_list.append(d)

listOfEntry = []
FamilyList = []
sen = []
sortlist=[]
sort = []
keylist=[]
counter = 1
num=1

path = "UnSpec Family"
if not os.path.exists(path):
    os.makedirs(path)
path1 = "Corpus"
if not os.path.exists(path1):
    os.makedirs(path1)
path2 = "Dictionary"
if not os.path.exists(path2):
    os.makedirs(path2)


for entry in dict_list:
    if(entry.get("Family")==""):
        continue
    
    if(entry.get("Family")!="" and entry.get("Class")==""):
        if(listOfEntry!=[]):
            f = open(os.path.join(path,"family{0}.txt".format(num)),"w")
            sortlist.append(sort)
            sort=[]
            for line in listOfEntry:
              hold = str(line,).strip('[]')
              hold = hold.replace("'","")
              f.write(json.dumps(hold))
              f.write("\n")
            counter += 1
            f.close()
            listOfEntry.clear()
            continue
        
    else:
        e = entry.get("Class Title")
        #f = entry.get("Class Definition")
        g = entry.get("Commodity Title")
        #h = entry.get("Commodity Definition")
        i = entry.get("Family")
        j= entry.get("Commodity")
        result = e +" " + g
        sen = sent_tokenize(result.lower())
        listOfEntry.append(sen)
        sort.append(j)
        num=int(i)
        e, f, g, h = "", "", "", ""

        
f = open(os.path.join(path,"family{0}.txt".format(num)),"w+")
sortlist.append(sort)
for line in listOfEntry:
    hold = str(line,).strip('[]')
    hold = hold.replace("'","")
    f.write(json.dumps(hold))
    f.write("\n")
counter += 1
f.close()
        

stop_words = set(stopwords.words('english'))
file_docs = []


anotherCount = 1
df1 = pd.DataFrame()
df2 = []
fam = []
path1 = os.path.join(path)
for file in os.listdir(path1):
    with open(os.path.join(path,file),'r', encoding='utf-8') as infile:
        txt = infile.readlines()
        for i in txt:
            fam.append(i) 
        df1 = df1.append(fam)
        df2.append(df1)
        df1 = pd.DataFrame()
        fam.clear()
        anotherCount += 1
       
alist =[]  

for data in df2:
    alist.append(data[0].tolist())
    

token =[]
Corlist=[]
Dictlist=[]
lengths=[]
inc = 1
ch = [ '``','``', "''",',','.','\\n',"'",";",":","(",")","-","--","\""]
for input in alist:
    for j in input:
        tokens = word_tokenize(j)
        tokens = [ j for j in tokens if not j in ch ]
        tokens = [w for w in tokens if not w in stop_words]
        tokens = [p.replace('.',"") for p in tokens]
        token.append(tokens)
    out_fname = "../Python/Corpus/corpus{0}".format(inc)
    tmp_fname = "../Python/Dictionary/dictionary{0}".format(inc)
    lengths.append(len(token))
    inc += 1
    dictionary = corpora.Dictionary(token)
    corpus = [dictionary.doc2bow(entry) for entry in token]
    token.clear()
    tf_idf = TfidfModel(corpus)
    cor_tf = tf_idf[corpus]
    MmCorpus.serialize(out_fname,cor_tf)
    Corlist.append(out_fname)
    dictionary.save_as_text(tmp_fname)
    Dictlist.append(tmp_fname)
    
    
print(f'Made the files and temp dictionary and corpus in {time.time() - start}')
