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
