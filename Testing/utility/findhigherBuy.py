def findhigherBuy(lst,lowestIndex):
    higherBuy = 0
    eligible = 0
    importance = [1,1,1,1,1]
    for i in range(lowestIndex+1,19):
        if lst[i] > 0:
            eligible += 1
            higherBuy += lst[i]*importance[eligible-1]
    return higherBuy
