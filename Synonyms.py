# This is testing the synonyms using NLTK

#importing
from nltk.corpus import wordnet

print("***************")

#declaring the word to find items for
word = "breathe"
#init the word
syns = wordnet.synsets(word)

#this will help later
print(syns[0].name())
#Prints word
print("\"" + syns[0].lemmas()[0].name() + "\" ")
#Prints def
print("Def: " + syns[0].definition()) 
print("***************")

#Finding synonyms
synonyms = [] 
antonyms = []   
  
for syn in wordnet.synsets(word): 
    for l in syn.lemmas(): 
        synonyms.append(l.name()) 
        if l.antonyms(): 
            antonyms.append(l.antonyms()[0].name()) 


print("***Synonyms***")
print(set(synonyms))
print("***Antonyms***")
print(set(antonyms))
print("***************")


#this makes it able to get the def of the syn
synUsed = synonyms[2]
syns2 = wordnet.synsets(synUsed)

#comparing two words
print("Synonym used: " + synUsed)
print("Def: ",  syns2[0].definition())
print("***************")

#this is the help later part
w1 = wordnet.synset(syns[0].name())
typeOfWord = syns[0].name()
secondPart = typeOfWord[-5:]
w2 = wordnet.synset(synonyms[2] + secondPart) 

percent = 100 * w1.wup_similarity(w2)
percent = round(percent, 2)


print(percent, "% simalirty in between the two words")
print("***************")