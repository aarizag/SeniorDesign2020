##
## Normalizing Data
## Jesse Rodriguez Avila
## Senior Design Project

#### reading data using pandas, converting data into array and lowercaseing data ####

import pandas as pd
# -------------------------------------------
## enter directory of new excel file --------
data = pd.read_excel("./County_List.xlsx")

# Create an Array from the spreadsheet
# use this array as main to manipulate data
new_array = []

for i in range(len(data)):
    # get data at column 2 row i
    # convert to Lower case
    
    # -----------------------------------------------------------------
    # ------- insert index of column here, replace 2 with new index ---
    new_array.append(data.iloc[:,2].iloc[i].lower())

#- Testing new array
#print(new_array[0].split())


# -- remove punctuation ---------------
import re
def punctuation_remove(tokenized_words):
    #tokeinzed means converting a sentence into an array of words.
    #every word in the array will then become a token
    punctuation_removed = []
    
    for i in range(len(tokenized_words)):
        #remove all punctuations from Token at index i
        new_word_without_punct = re.sub(r'[^\w\s]', '', tokenized_words[i])
        
        # if the word is not blank append to new array
        if new_word_without_punct != '':
            punctuation_removed.append(new_word_without_punct)
            
    return punctuation_removed


# -- Remove Stop words ---------------
from nltk.corpus import stopwords
def stopwords_remove(tokenized_words):
    #array with stopwords removed
    stopwords_removed = []

    # remove stop words from tokenized sentence
    stopwords_englishLanguage = set(stopwords.words('english'))
    
    for i in range(len(tokenized_words)):
        if tokenized_words[i] not in stopwords_englishLanguage:
            stopwords_removed.append(tokenized_words[i])
    
    return stopwords_removed


# -- lematization ---------------
from nltk.stem import WordNetLemmatizer 
def lematization(tokenized_words):
    # convert list of tokenized words into normalized form
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for i in range(len(tokenized_words)):
        lemma = lemmatizer.lemmatize(tokenized_words[i], pos='v')
        lemmas.append(lemma)
    return lemmas


# convert all data to lowercase 
# remove all punctuation
# remove stop words
# use lexicon normalization (Lemmatization) to change any verb into its normalized form

# Example: remove punctuation
print(punctuation_remove("The sa/!@#$%^&*m.e i's not".split()))

# Example: remove stopwords
print(stopwords_remove("This is not multiplying".split()))

# Example: lematization (change any verb into its normalized form)
print(lematization("adding multiplying".split()))

# final Part: normalizing_data
def normalizing_data(tokenized_words):
    normalized = lematization(stopwords_remove(punctuation_remove(tokenized_words)))
    return normalized

# printing test run
#print(normalizing_data("This is not multiplying".split()))


from nltk.tokenize import word_tokenize
# example of word being normilazed
print("\n\n\nNormalizing data Example")
print("---------------------------------------------------------------")
print(word_tokenize(new_array[0]))
print(normalizing_data(word_tokenize(new_array[0])))
print("---------------------------------------------------------------")


#### Normalizing all data in new_array ####
#------------------------------------------

# array with normalized data
array_NormalizedData = []

for i in range(len(new_array)):
    tokenized = word_tokenize(new_array[i])
    array_NormalizedData.append(normalizing_data(tokenized))
    



# Print data in newline (better to visualized)
print("\nArray with normalized data")
print("---------------------------------------------------------------")
for i in range(len(array_NormalizedData)):
    print(array_NormalizedData[i])
print("---------------------------------------------------------------")