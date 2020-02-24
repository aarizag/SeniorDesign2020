import os
import xlsxwriter
from xlrd import open_workbook
from gensim.models import LsiModel
from gensim import similarities,models
import gensim
from gensim.corpora import MmCorpus
import warnings
import time
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from gensim import corpora
import operator
import pdb
warnings.simplefilter('ignore')

import MakerOfFiles as mf

book = open_workbook('ignore/eCAPS_COMM_11072019.xlsx')
#book = open_workbook('ignore/County_List.xlsx')
county_list = []
#for testing you need 0. real you will need 1
sheet = book.sheet_by_index(1)
# read header values into the list
keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

for row_index in range(1, sheet.nrows):
    d = {keys[col_index]: sheet.cell(row_index, col_index).value
         for col_index in range(sheet.ncols)}
    #Uncomment these for real use
    county_list.append(d)



def reduceList2(lengths,sortlist, dictionarys,corpuses,county):
    listNew = []
    query_doc= word_tokenize(county.lower())
    mm = MmCorpus(corpuses)
    tf_idf = models.TfidfModel(mm)
    cortfidf = tf_idf[mm]
    load_dic = corpora.Dictionary.load_from_text(dictionarys)
    lsi = LsiModel(mm,num_topics=lengths,id2word = load_dic,chunksize=1000)
    index = gensim.similarities.MatrixSimilarity(lsi[mm],num_features=lengths)
    query_doc_bow = load_dic.doc2bow(query_doc, True)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    sim = list(zip(sortlist,index[lsi[query_doc_tf_idf]]))
    sim.sort(key = operator.itemgetter(1),reverse = True)
    for a in sim:
        if(a[0]==''):
            continue
        elif(a[1]>0.1):
            listNew.append(a)
                
    #excelSheet = workbook.add_worksheet(str(sheet))
    cot = 1
    for piece in listNew:
        excelSheet.write(cot,0,piece[0])
        excelSheet.write(cot,1,piece[1])
        cot+=1


start2=time.time()
workbook   = xlsxwriter.Workbook('../Python/ignore/Result.xlsx')

for w in county_list:
    excelSheet = workbook.add_worksheet(str(w.get('COMM_CLS')))
    for i in range(len(mf.lengths)):
        reduceList2(mf.lengths[i],mf.sortlist[i],mf.Dictlist[i],mf.Corlist[i],str(w.get('KEYWD')))
        #print(i)
    
workbook.close()       
print(f'Narrowing done in {time.time() - start2}')



"""

import os
from gensim.models import LsiModel
from gensim import similarities,models
import gensim
from gensim.corpora import MmCorpus
import warnings
import time
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from gensim import corpora
import operator
warnings.simplefilter('ignore')

import MakerOfFiles as mf

test = "MASS TRANSPORTATION - RAIL VEHICLE PARTS AND ACCESSORIES"
test = test.lower()
query_doc = word_tokenize(test)


listNew = []


def reduceList(lengths,sortlist, dictionarys,corpuses):
    for i in range(len(lengths)):
        mm = MmCorpus(corpuses[i])
        tf_idf = models.TfidfModel(mm)
        load_dic = corpora.Dictionary.load_from_text(dictionarys[i])
        lsi = LsiModel(mm,num_topics=lengths[i],id2word = load_dic)
        index = gensim.similarities.MatrixSimilarity(lsi[mm],num_features=lengths[i])
        query_doc_bow = load_dic.doc2bow(query_doc, True)
        query_doc_tf_idf = tf_idf[query_doc_bow]
        sim = list(zip(sortlist[i],index[lsi[query_doc_tf_idf]]))
        sim.sort(key = operator.itemgetter(1),reverse = True)
        listNew.append(sim[0:5])
        

start2=time.time()
reduceList(mf.lengths,mf.sortlist,mf.Dictlist,mf.Corlist)
    
       
print(f'Narrowing done in {time.time() - start2}')

exceltest = pd.ExcelWriter("test2.xlsx",engine='xlsxwriter')
data= pd.DataFrame(listNew)
data.to_excel(exceltest,sheet_name='MASS TRANSPORTATION')

exceltest.save()

"""
