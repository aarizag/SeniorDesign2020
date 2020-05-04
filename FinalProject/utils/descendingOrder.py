## Both these Algorithms Will sort the list in Descending Order

####### Instructions ####### 
############################

    ## Parameters must be in this formatt: a list of list containing ["standard title", similarity score]

    # list_ = [['bomb protection devices supplies', 29.85714285714286],
    #         ['power supply outlet strip', 80.71428571428572],
    #         ['bag sealing tools equipment', 87.58823529411765],
    #         ['network system equipment rack', 86.17857142857143],
    #         ['hospital equipment power columns', 84.87394957983193],
    #         ['hospital equipment instrument panels', 87.33823529411765]]

    # SelectionSort(list_)
    # mergeSort(list_)

#### End of Instructions ### 
############################

## as of now its time complexity is O(n^2)
## I will implement a better one later, this was just a 
## quick implementation for testing purposes
def SelectionSort(array):
    counter = 0
    for i in range( len(array) ):
        index_of_smallest = 0
        for j in range( len(array) - counter ):
            if(array[j][1] < array[index_of_smallest][1]):
                index_of_smallest = j
                
        temp = array[index_of_smallest]
        array[index_of_smallest] = array[len(array) - counter - 1]
        array[len(array) - counter - 1] = temp
        counter +=1

########################################
## Updated Sorting Algorithm: 04/25/2020
## Merge Sort: time complexity O(nlogn)
def mergeSort(unsortedList): 
    if (len(unsortedList) > 1): 
        left_side = unsortedList[0:(int(len(unsortedList) / 2))]  
        right_side = unsortedList[(int(len(unsortedList) / 2)):len(unsortedList)] 
  
        mergeSort(left_side) # Sorting left half 
        mergeSort(right_side) # Sorting right half 
  
        i = 0
        j = 0
        k = 0
          
        # temp arrays 
        while (j < len(right_side) and i < len(left_side)): 
            if left_side[i][1] > right_side[j][1]: 
                unsortedList[k] = left_side[i] 
                i+=1
            else: 
                unsortedList[k] = right_side[j] 
                j+=1
            k+=1
          
        while (len(left_side) > i): 
            unsortedList[k] = left_side[i] 
            i+=1
            k+=1
          
        while (len(right_side) > j): 
            unsortedList[k] = right_side[j] 
            j+=1
            k+=1