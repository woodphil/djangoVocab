def calculateLevenshtein(word1, word2):
    #only works in one direction
    if len(word1) > len(word2):
        word1,word2 = word2,word1
    
    #create and initialize a 2d array
    cost = 100
    total = [[0 for i in range(len(word2))] for j in range(len(word1))]
    for i in range(len(word1)):
        for j in range(len(word2)):
            # calculate the cost of the current location
            if word1[i] != word2[j]:
                cost = 1
            else:
                cost = 0
            
            # base cases
            if i==0 and j==0:
                total[i][j] = cost
            elif i==0 and j!=0:
                total[i][j] = total[i][j-1] + cost
            elif i!=0 and j==0:
                total[i][j] = total[i-1][j] + cost
            else:
                total[i][j] = min(total[i-1][j], total[i-1][j-1], total[i][j-1]) + cost
    return total[len(word1)-1][len(word2)-1]    
if __name__=="__main__":
    from sys import argv
    print(calculateLevenshtein(argv[1],argv[2]))