import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from xlrd import open_workbook
import gensim
import numpy as np

book = open_workbook('./ignore/eCAPS_COMM.xlsx')
#book = open_workbook('./ignore/UNSPSC English v220601 project.xlsx')
dict_list = []
sheet = book.sheet_by_index(2)
# read header values into the list
keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

for row_index in range(1, sheet.nrows):
    d = {keys[col_index]: sheet.cell(row_index, col_index).value
         for col_index in range(sheet.ncols)}
    dict_list.append(d)

    """
listofSegments = []
segmentSet= set()
familySet=[0]
classSet=[]
familySet1=0
classSet1=0
commoditySet=0
temp = "12345678"
for entry in dict_list:
    a = str(int(entry.get("Segment")))
    if(a not in segmentSet):
        segmentSet.add(a)
        #familySet.pop(0)
        #listofSegments.append([temp,familySet])
        listofSegments.append([temp,familySet1,classSet1,commoditySet])
        temp=a
        #familySet,classSet,commoditySet = [],[],0
        familySet1,classSet1,commoditySet = 0,0,0
    b = entry.get("Family")
    c = entry.get("Class")
    d = entry.get("Commodity")
    if( b != '' and c ==''):
        #familySet.append((1,classSet))
        #classSet=[]
        familySet1 += 1
    elif(c !='' and d ==''):
        #classSet.append((1,commoditySet))
        #commoditySet=0
        classSet1 += 1
    else:
        commoditySet += 1
    
#listofSegments.append([temp,familySet])
listofSegments.append([temp,familySet1,classSet1,commoditySet])
listofSegments.pop(0)

familys = 0
classes=0
com =0

for i in listofSegments:
    print(i)
    familys += i[1]
    classes += i[2]
    com += i[3]

print(len(listofSegments))
print(familys)
print(classes)
print(com)


for i in listofSegments:
    print(i[0])
    for j in i[1]:
        print(j)

        
"""
temp2 = 0
county=[]
for entry in dict_list:
    a=entry.get("COMM_CLS")
    county.append(int(a))
numb=[]
num = 1
for i in range(0,len(county)-1):
    if(county[i]==county[i+1]):
       num += 1
    elif(county[i]!=county[i+1]):
        numb.append(num)
        num=1


print(numb)
print(min(numb))
print(max(numb))
