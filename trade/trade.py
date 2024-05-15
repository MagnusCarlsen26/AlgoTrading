def trade(lst):
    def findLowest(lst):
        lowestIndex = -1
        for i in range(19):
            if lst[i] != 0:
                lowestIndex = i
                break
        return lowestIndex,lst[lowestIndex],(lowestIndex+1)/2

    def findhigherBuy(lst):
    
        higherBuy = 0
        for i in range(lowestIndex+1,19):
            if lst[i] > 0:
                higherBuy += lst[i]
        return higherBuy

    ratio = 7

    lowestIndex,lowerBuy,buyCost = findLowest(lst)
    if lowestIndex == -1:
        return

    higherBuyQuantity = findhigherBuy(lst)
    if higherBuyQuantity == 0:
        return
    if higherBuyQuantity/lowerBuy > ratio:
        print('BUY',time,buyCost)
        return
