
import numpy as np

# The longest palindromic subsequence in seq 
def exercise_4(str): 
    
    n = len(str) 
  
    # Initialize the matrix in zeros
    matrix = [[0 for x in range(n)] for x in range(n)] 
  
    # Put 1 in the diagonal because for i = j the character is the same so
    # by its own is a palindromic string
    for i in range(n): 
        matrix[i][i] = 1
  
   # we want to move diagonically so we iterate for two 
    # variable to get the result we need. In the code that follows we check 
    # all the characters in the string and their position and "score" how many
    # have the same reading 
    #pali = ""
    for d1 in range(2, n + 1): 
        for d2 in range(n-d1 + 1): 
            j = d2 + d1 -1
            if str[d2] == str[j] and d1 == 2: 
                matrix[d2][j] = 2
                #pali = pali + str[d2]
            elif str[d2] == str[j]: 
                matrix[d2][j] = matrix[d2 + 1][j-1] + 2
                #pali = pali + str[d2]
            else: 
                matrix[d2][j] = max(matrix[d2][j-1], matrix[d2 + 1][j]) 
    
    len_seq = np.max(matrix)
    
    #print(pali)
    #ilap = ""
    #if len_seq % 2 == 0:
    #    for i in range(len(pali)):
    #        ilap = ilap + pali[len(pali)-1-i]
    #    print("The palindrome word in ", str, " is ", ilap+pali,
    #              ". So the times a subsequence character appears is ", np.max(matrix) )
    #else:
    #    for i in range(len(pali)):
     #       ilap = ilap + pali[len(pali)-1-i]
    #    print("The palindrome word in ", str, " starts and ends with ", ilap+pali, ". So the times a subsequence character appears is ", np.max(matrix) )

    return len_seq
  
stringa = 'DATAMININGSAPIENZA'
exercise_4(stringa)
