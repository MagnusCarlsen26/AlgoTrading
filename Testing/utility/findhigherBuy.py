def findhigherBuy(lst,lowestIndex):
    higherBuy = 0
    for i in range(lowestIndex+1,19):
        if lst[i] > 0:
            higherBuy += lst[i]
    return higherBuy
