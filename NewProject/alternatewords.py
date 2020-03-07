def listToAscendingOrder(newList2):
    #print("# puts list in ascending order")
    index_OfGreatest = 0
    counter = 0

    for i in range(len(newList2)):
        # Find index of greatest value
        for j in range(len(newList2) - counter):
            if(newList2[index_OfGreatest][1] < newList2[j][1]):
                index_OfGreatest = j

        # use index found to switch greatest index with (last - counter)
        if(i != 0):
            temp = newList2[index_OfGreatest]
            newList2[index_OfGreatest] = newList2[len(newList2) - (counter + 1)]
            newList2[len(newList2) - counter] = temp

        # increase the counter and reset index of greatest to 0
        counter += 1
        index_OfGreatest = 0


## Euclidean Distance
#  - distance between two vectors
import math
def euclidean_distance(u, v):
    summation = 0
    for i in range(len(u)):
        # (u1 - v1)^ 2
        summation += ((u[i] - v[i]) * (u[i] - v[i]))
    # squareroot result of summation
    euclidean_distance = math.sqrt(summation)
    return euclidean_distance
# Example       
print(euclidean_distance([1,2,3], [4,5,6]))


## Load Google's Pre-Trained Dataset
##
import wordNet
import gensim.models.word2vec as word2vec

from gensim.models import KeyedVectors

# Google's Pre-Trained Data Set
from gensim.models import KeyedVectors
file_directory = '../ignore/GoogleNews-vectors-negative300.bin.gz'
# Googles Pre-trained data set has 300 futures
model = KeyedVectors.load_word2vec_format(file_directory, binary=True)

print("## Done loading Google's Pre-Trained Word2Vec model")


sentence_1_normalized = 'school supply set kit' 
sentence_2_normalized = 'school equipment supply'
from nltk.tokenize import word_tokenize as tokenize_sentence
sentence_1_tokenized = tokenize_sentence(sentence_1_normalized)
sentence_2_tokenized = tokenize_sentence(sentence_2_normalized)


## Word embedding
##
# Using Google's pre-train dataset, convert every word in the tokenized sentence into its 
# position coordinates in a 300 dimension vector space
def word_embedding(tokenized_sentence):
    list_wordembedding = []
    for token in tokenized_sentence:
        list_wordembedding.append(model[token]) 
    return list_wordembedding
        
# word_embedding() takes in a tokenized sentence 
# this function will return a list of list containing
# the vector position of every word in a sentece



#parameter = two normalized sentences
def list_vectorPosition(tokenized_sentence1, tokenized_sentence2):
    # list at index 0 = sentence 1
    # list at index 1 = sentence 2
    list1 = []
    # the vector position of every word in a sentece
    sentence1_vector_position = word_embedding(tokenized_sentence1) # vector position for every word in sentence 1
    sentence2_vector_position = word_embedding(tokenized_sentence2) # vector position for every word in sentence 1
    list1.append(sentence1_vector_position)
    list1.append(sentence2_vector_position)
    return list1

#list_vectorPosition returns a (list) containing a (list) of (list with 300 values).
#list_vectorPosition[0] vector positions for sentence 1
#list_vectorPosition[1] vector positions for sentence 2
#list_vectorPosition[0][i] returns a list with vector position (300 entries) of word at i

list1 = list_vectorPosition(sentence_1_tokenized, sentence_2_tokenized)


def compare(tokenized_sentence1, tokenized_sentence2, list_of_vector_position):
    # index 0 = sentence 1
    # index 1 = sentence 2
    compareFrom = tokenized_sentence1
    compareTo = tokenized_sentence2
    compareFrom_vector = 0 #list_of_vector_position[0]
    compareTo_vector = 1 #list_of_vector_position[1]
    if (len(tokenized_sentence1) < len(tokenized_sentence2)):
        compareFrom = tokenized_sentence2
        compareTo = tokenized_sentence1
        compareFrom_vector = 1 # list_of_vector_position[1]
        compareTo_vector = 0 # list_of_vector_position[0]
    
    index_of_most_similar = 0 # j
    distance_of_most_similar = 10000
    
    results = []
    
    for i in range( len(list_of_vector_position[compareFrom_vector]) ):
        for j in range( len(list_of_vector_position[compareTo_vector]) ):
            current_distance = euclidean_distance(list_of_vector_position[compareFrom_vector][i], list_of_vector_position[compareTo_vector][j])
            
            if(distance_of_most_similar > current_distance):
                index_of_most_similar = j
                distance_of_most_similar = current_distance
                
        results.append( [compareFrom[i], compareTo[index_of_most_similar], distance_of_most_similar] )
        index_of_most_similar = 0
        distance_of_most_similar = 10000
        
    return results
    
    
print("Done!")


results = compare(sentence_1_tokenized, sentence_2_tokenized, list1)

def removeDistanceScore(list_results):
    newList = []
    for list in list_results:
        newList.append(list[:-1])
    return newList
results_NoScore = removeDistanceScore(results)
print(results_NoScore)

def compareResults(sentence_1_normalized, sentence_2_normailzed):
    # tokenize normalized sentences
    s1_t = tokenize_sentence(sentence_1_normalized) # tokenize sentence 1
    s2_t = tokenize_sentence(sentence_2_normailzed) # tokenize sentence 2

    list1_final = list_vectorPosition(s1_t, s2_t) # list with vector positions of every word in both sentences
    
    results_Final = compare(s1_t, s2_t, list1_final) # return list with nearest neighbors and distance score
    
    results__final_NoScore = removeDistanceScore(results_Final) # remove score list from results
    
    return results__final_NoScore



# load our UNSPSC from our manual comparisons
import pandas as pd

unspsc_column = 1

unspsc = pd.read_excel('Result6.xlsx',sheet_name='785').iloc[:,0]
ecomm = pd.read_excel('../ignore/eCAPS_COMM_11072019.xlsx',sheet_name='COMM_ITM').iloc[:,5]


eCOMM_Line = ecomm.iloc[6057].lower()
print(eCOMM_Line)
print("----------------------------------------------------")
def percentage_similarity(eCOMM_line_, unspsc_):
    list_t = []
    for i in range( len(unspsc_)):
        #print(unspsc.iloc[i])
        current_result = compareResults(eCOMM_line_, unspsc_.iloc[i]) # compare a ecomm line to the current line from UNSPSC
        newlist = [unspsc_.iloc[i], wordNet.average_percentage(current_result)]
        list_t.append( newlist )
    return list_t 
    
sim_percentage1 = percentage_similarity(eCOMM_Line, unspsc)
listToAscendingOrder(sim_percentage1)

printList(sim_percentage1)

eCOMM_Line1 = ecomm.iloc[6056].lower()
print(eCOMM_Line1)
print("--------------------------------------------")
sim_percentage2 = percentage_similarity(eCOMM_Line1, unspsc)
listToAscendingOrder(sim_percentage2)
printList(sim_percentage2)



