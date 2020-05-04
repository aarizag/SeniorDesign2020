import utils.similarityPercentage as SimilarityPercentage
import math
import gensim.models.word2vec as word2vec
from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize as tokenize_sentence
import pandas as pd




## Sorts final results in Descending Order
## Import descendingOrder.py script
##      - SelectionSort(unsortedList)
##      - mergeSort(unsortedList)
print("\n_____________________________________________")
#print("Loading... descendingOrder.py Script")
#import descendingOrder as sort
#print("Successfully loaded: descendingOrder.py")

## Euclidean Distance
#  - distance between two vectors
def euclideanDistance(u, v):
    summation = 0
    for i in range(len(u)):
        # (u1 - v1)^ 2
        summation += ((u[i] - v[i]) * (u[i] - v[i]))
    # squareroot result of summation
    euclidean_distance = math.sqrt(summation)
    return euclidean_distance
# Example       
#print(euclidean_distance([1,2,3], [4,5,6]))

## Print List in a column format
def printList(lists):
    for current_list in lists:
        print(current_list)

####################################
## Load Google's Pre-trained Dataset


# Google's Pre-Trained Data Set
file_directory = '../models/'
file_name = 'GoogleNews-vectors-negative300.bin.gz'
print("\nLoading... " + file_name)

# Googles Pre-trained data set has 300 futures (300 neural network neurons)
model = KeyedVectors.load_word2vec_format(file_directory + file_name, binary=True)
print("Load successfully: Google's Pre-trained Word2Vec model\n")

## Word embedding
##
# Using Google's pre-train dataset, convert every word in the tokenized sentence into its 
# position coordinates in a 300 dimension vector space
def wordEmbedding(tokenized_sentence):
    list_wordembedding = []
    for token in tokenized_sentence:
        try:
            list_wordembedding.append(model[token]) 
        except:
            # if the word does not exist in Googles data set
            # set "company" as default
            # This is temporary
            list_wordembedding.append(model["company"]) 
        
    return list_wordembedding
# word_embedding() takes in a tokenized sentence 
# this function will return a list of list containing
# the vector position of every word in a sentece


# parameter = two normalized sentences
def listVectorPositions(tokenized_sentence1, tokenized_sentence2):
    # list at index 0 = sentence 1
    # list at index 1 = sentence 2
    temp = []
    # the vector position of every word in a sentece
    sentence1_vector_positions = wordEmbedding(tokenized_sentence1) # vector position for every word in sentence 1
    sentence2_vector_positions = wordEmbedding(tokenized_sentence2) # vector position for every word in sentence 1
    
    temp.append(sentence1_vector_positions)
    temp.append(sentence2_vector_positions)
    return temp
#list_vectorPosition returns a (list) containing a (list) of (list with 300 values).
#list_vectorPosition[0] vector positions for sentence 1
#list_vectorPosition[1] vector positions for sentence 2
#list_vectorPosition[0][i] returns a list with vector position (300 entries) of word at i


## Creating Pairs: This function will determine what words from one standard 
##                 will be comapared to what words from the other standard
def createPairs(tokenized_sentence1, tokenized_sentence2, list_of_vector_position):
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
    distance_of_most_similar = 1000000 ## we chose a random big number, can also use the max value an int can hold
    
    results = []

    for i in range( len(list_of_vector_position[compareFrom_vector]) ):
        for j in range( len(list_of_vector_position[compareTo_vector]) ):
            current_distance = euclideanDistance(list_of_vector_position[compareFrom_vector][i], list_of_vector_position[compareTo_vector][j])
            
            if(distance_of_most_similar > current_distance):
                index_of_most_similar = j
                distance_of_most_similar = current_distance
                
        results.append( [compareFrom[i], compareTo[index_of_most_similar], distance_of_most_similar] )
        index_of_most_similar = 0
        distance_of_most_similar = 1000000
        
    return results


## I made this function so that it can be easier comparing. this function will tokenized both sentence, find 
## its vector positions for each word, and compare to see what pair of words will be compared to eachother
## All we have to enter as a Parameter is two normalized standards, the function will do the rest
def startPairingWords(sentence_1_normalized, sentence_2_normailzed):
    # tokenize normalized sentences
    s1_t = tokenize_sentence(sentence_1_normalized) # tokenize sentence 1
    s2_t = tokenize_sentence(sentence_2_normailzed) # tokenize sentence 2

    list_VP = listVectorPositions(s1_t, s2_t) # list with vector positions of every word in both sentences
    
    pairs = createPairs(s1_t, s2_t, list_VP) # return list with nearest neighbors and distance score
    
    return pairs


## import script similarityPercentage.py
## Calculate Percentage Similarity from list of paired words
## To Start calculating we must first import our similarityPercentage.py python file

# import similarityPercentage.py script, it will find similarity percentage
#print('Loading... similarityPercentage.py')
#print('Load Successfully: similarityPercentage.py')
#print("_____________________________________________")
#print("MAIN FUNCTION: comparisons() ")



###################################################
###################################################
####### This is the MAIN FUNCTION #################
###################################################
###################################################
## This is the main function to compare and calculate similarity percentage

#For single two single sentences to compare and return the float of how similar
def comparisons(eCOMM_line_, unspsc_):
    results = []
    ListofPairs = startPairingWords(eCOMM_line_, unspsc_) # compare a ecomm line to the current line from UNSPSC
    return SimilarityPercentage.average(ListofPairs)
   
#print("_____________________________________________\n")

#Used with the wordinUnspsc
def comparisons2(eCOMM_line_, unspsc_):
    results = []
    for i in range( len(unspsc_)):
        ListofPairs = startPairingWords(eCOMM_line_, unspsc_.iloc[i]) # compare a ecomm line to the current line from UNSPSC
        tempList = [unspsc_.iloc[i], SimilarityPercentage.average(ListofPairs)]
        results.append( tempList )
    return results 


## New one ############################

#narrowed_down_UNSPSC = pd.read_excel("../ignore/Result6.xlsx",sheet_name='475').iloc[:,0]
#print("Done loading Narrowed-down list!")
#narrowed_down_UNSPSC
#string = "DISPOSABLE GOWNS MASKS"
#string2 = "masks plate hair grow"

#newOutput = comparisons(string.lower(), string2)
#print(newOutput)
#sort.mergeSort(newOutput)
#printList(newOutput)

## Old one ##############################

#narrowed_down_UNSPSC = pd.read_excel("../ignore/Result6.xlsx",sheet_name='475').iloc[:,0]
#print("Done loading Narrowed-down list!")
#narrowed_down_UNSPSC
#string = "DISPOSABLE GOWNS MASKS"

#newOutput = percentage_similarity(string.lower(), narrowed_down_UNSPSC)
#descending_order(newOutput)
#printList(newOutput)

#########################################
#print("_____________________________________________")
