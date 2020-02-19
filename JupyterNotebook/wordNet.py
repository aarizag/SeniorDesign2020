from nltk.corpus import wordnet

# find similarity percentange between two words
# takes in two list as a parameter, each list has syns of the current word
def similarity_percentage(word1, word2):
    percent_most_similar = 0# word1[0].wup_similarity(word2[0])
        
    if (percent_most_similar is None or percent_most_similar == None):
        return 0

    for i in range(len(word1)):
        word1_syn = word1[i]
        for j in range(len(word2)):
            word2_syn = word2[j]
            wupSimilar = word1_syn.wup_similarity(word2_syn)
            if (wupSimilar is not None or wupSimilar != None):
                if (percent_most_similar < wupSimilar):
                    percent_most_similar = wupSimilar
                #print( str(wupSimilar * 100) + "% similarity - " + str(word1[i]) + " and " + str(word2[j]) )
        #print("-------------------------------------------------------------------")
    return percent_most_similar


## takes in a list of list containing what two words are similar
## Example: 
## [['president', 'leader'], ['greets', 'speaks'], ['press', 'media'], ['chicago', 'illinois']]   
def results(list_of_lists):
    results = []
    for i in range(len(list_of_lists)):
        word1_s1 = wordnet.synsets(list_of_lists[i][0]) 
        word2_s2 = wordnet.synsets(list_of_lists[i][1]) 
        #print(word1_s1)
        #print(word2_s2)
        if (len(word1_s1) != 0 and len(word2_s2) != 0):
            percentage = similarity_percentage(word1_s1, word2_s2)
            results.append( [list_of_lists[i][0], list_of_lists[i][1], percentage * 100] )
        else:
            results.append( [list_of_lists[i][0], list_of_lists[i][1], 0] )

    return results

# Find average percentage

def average_percentage(list_of_list):
    lists3 = results(list_of_list)
    l = len(list_of_list)
    percent = 0

    for list1 in lists3:
        percent += list1[2]

    return percent / l