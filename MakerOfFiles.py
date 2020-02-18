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
from gensim.models import LsiModel
from gensim import similarities
import gensim
from gensim.corpora import MmCorpus
import warnings
import time

warnings.simplefilter('ignore')

start=time.time()
book = open_workbook('ignore/UNSPSC English v220601 project.xlsx')
#book = open_workbook('ignore/Unspec List2b.xlsx')

dict_list = []
sheet = book.sheet_by_index(0)
# read header values into the list
keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

for row_index in range(1, sheet.nrows):
    d = {keys[col_index]: sheet.cell(row_index, col_index).value
         for col_index in range(sheet.ncols)}
    d.pop('Synonym')
    d.pop('Acronym')
    dict_list.append(d)

    
    
path = "UnSpec Family"

if not os.path.exists(path):
    os.makedirs(path)

ch = [ '``','``', "''",',','.','\\n',"'",";",":","(",")","-","--"]
stop_words = set(stopwords.words('english'))

sortlist=[]
sort = []
listOfEntry = []
sen = []
token =[]
Corlist=[]
Dictlist=[]
lengths=[]
num=1
inc = 1

for entry in dict_list:
    if(entry.get("Family")==""):
        continue
    if(entry.get("Family")!="" and entry.get("Class")==""):
        if(listOfEntry!=[]):
            f = open(os.path.join(path,"family{0}.txt".format(num)),"w")
            sortlist.append(sort)
            for line in listOfEntry:
                sen = sent_tokenize(line)
                for j in sen:
                    tokens = word_tokenize(j)
                    tokens = [ j for j in tokens if not j in ch ]
                    tokens = [w for w in tokens if not w in stop_words]
                    tokens = [p.replace('.',"") for p in tokens]
                    token.append(tokens)
                hold = str(line).strip('[]')
                hold = hold.replace("'","")
                f.write(json.dumps(hold))
                f.write("\n")
            f.close()
            listOfEntry.clear()
            out_fname = get_tmpfile("corpus{0}".format(inc))
            tmp_fname = get_tmpfile("dictionary{0}".format(inc))
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
            continue
    else:
        e = entry.get("Class Title")
        f = entry.get("Class Definition")
        g = entry.get("Commodity Title")
        h = entry.get("Commodity Definition")
        i = entry.get("Family")
        j= entry.get("Commodity")
        if(f != "" and h != ""):
            result = e+". "+f+". "+g+". "+h+". "
        elif(f != "" and h == ""):
            result = e+". "+f+". "+g+". "+h
        elif(f == "" and h != ""):
            result = e+". "+f+" "+g+". "+h+". "
        else:
            result = e + ". " + f + "" + g + ". " + h
        listOfEntry.append(result.lower())
        sort.append(j)
        num=int(i)
        e, f, g, h = "", "", "", ""

        
f = open(os.path.join(path,"family{0}.txt".format(num)),"w")
sortlist.append(sort)
for line in listOfEntry:
    sen = sent_tokenize(line)
    for j in sen:
        tokens = word_tokenize(j)
        tokens = [ j for j in tokens if not j in ch ]
        tokens = [w for w in tokens if not w in stop_words]
        tokens = [p.replace('.',"") for p in tokens]
        token.append(tokens)
    hold = str(line).strip('[]')
    hold = hold.replace("'","")
    f.write(json.dumps(hold))
    f.write("\n")
out_fname = get_tmpfile("corpus{0}".format(inc))
tmp_fname = get_tmpfile("dictionary{0}".format(inc))
lengths.append(len(token))
dictionary = corpora.Dictionary(token)
corpus = [dictionary.doc2bow(entry) for entry in token]
tf_idf = TfidfModel(corpus)
cor_tf = tf_idf[corpus]
MmCorpus.serialize(out_fname,cor_tf)
Corlist.append(out_fname)
dictionary.save_as_text(tmp_fname)
Dictlist.append(tmp_fname)
f.close()
listOfEntry.clear()
token.clear()

print(f'Made the files and temp dictionary and corpus in {time.time() - start}')