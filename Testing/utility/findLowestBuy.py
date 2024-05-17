def findLowestBuy(lst):
    lowestIndex = -1
    for i in range(19):
        if lst[i] != 0:
            lowestIndex = i
            break
    return lowestIndex,lst[lowestIndex],(lowestIndex+1)/2
