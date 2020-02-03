import nltk,re,pprint
import os
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim
from nltk.corpus import stopwords
from nltk.corpus import wordnet


sentence = "the man is wearing different colored hose. the gentleman garments are alternet dyed socks. the male is clothes on his feet are multicolored. the female socks are polychromatic. the maiden is clothes on his feet are multicolored. the madam garments are alternet dyed socks."


sen = sent_tokenize(sentence)
list1=[]

stop_words = set(stopwords.words('english'))

for i in sen:
    sen2 = word_tokenize(i)
    sen2 = [w for w in sen2 if not w in stop_words]
    list1.append(sen2)

print(len(list1))



dictionary = gensim.corpora.Dictionary(list1)
corpus = [dictionary.doc2bow(entry) for entry in list1]

tf_idf = gensim.models.TfidfModel(corpus)


sims = gensim.similarities.Similarity('dir', tf_idf[corpus], num_features=len(dictionary))

test = " the woman is wearing different colored socks"

query_doc = word_tokenize(test)
query_doc = [w for w in query_doc if not w in stop_words]
query_doc_bow = dictionary.doc2bow(query_doc, True)

query_doc_tf_idf = tf_idf[query_doc_bow]

print(max(sims[query_doc_tf_idf]))


#this will be the part where we get the sysnonyms for the word in each list.

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

listofSysn = []

print(query_doc)
for w in query_doc:
    choice = w
    words = [] #List to store rating of the product
    driver = webdriver.Chrome()
    driver.get("https://www.merriam-webster.com/thesaurus/"+choice+"")
    content = driver.page_source
    soup = BeautifulSoup(content)
    a = soup.find('div', attrs={'class':'thes-list-content synonyms_list'})
    for i in a.find('ul',{'class':'mw-list'}):
            name = i.text
            words.append(name.replace(',','').rstrip())
    listofSysn.append(words)
    driver.quit()

print(listofSysn)

"""

#just to narrow down words
#a way to find out to narrow words for making new list entry.

from nltk.corpus import wordnet


def howSimaliryTheyAre(a,b):
    syns = wordnet.synsets(a)
    syns2 = wordnet.synsets(b)
    #this is the help later part
    w1 = wordnet.synset(syns[0].name())
    typeOfWord = syns[0].name()
    secondPart = typeOfWord[-5:]
    w2 = wordnet.synset(syns2[0].name())
    percent = 100 * w1.wup_similarity(w2)
    percent = round(percent, 2)
    return percent



print("These two word are simalirty by ",howSimaliryTheyAre("accreditation","certification"))


#this part is for testing to see if i could look up alternate list with synonyms
#comment this out only used for testing for now

import os
import json
newlisttocompare = []
listofPercent = []
templist=[['feminine', 'womanish', 'womanlike', 'womanly'], ['sock', 'stocking'], ['chromatic', 'colored', 'colorful', 'kaleidoscopic', 'motley', 'multicolored', 'multihued', 'polychrome', 'prismatic', 'rainbow', 'varicolored', 'varied', 'variegated', 'various']]
count = 0
count2 = 1
testdict = {}
query = ['female', 'hose', 'polychromatic']
q2 = query

print(len(templist))

f = open("listS","w+")

for b in templist:
    temp=query[count]
    for c in b:
        q2[count]=c
        testdict.update({count2:q2})
        print(testdict)
        f.write(json.dumps(testdict))
        count2 += 1
        testdict.clear()
    q2[count]= temp
    count += 1


"""
