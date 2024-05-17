def findhigherBuy(lst,lowestIndex):
    higherBuy = 0
    for i in range(lowestIndex+1,19):
        if lst[i] > 0:
            higherBuy += lst[i]
    return higherBuy

def findLowestBuy(lst):
    lowestIndex = -1
    for i in range(19):
        if lst[i] != 0:
            lowestIndex = i
            break
    return lowestIndex,lst[lowestIndex],(lowestIndex+1)/2


def trade(df,stopLoss,bookprofit,buyCondition,sellCondition,toBuy=1,buyAmount=0,profit=0,request_number=-1):
    global total_profit
    while request_number < len(df)-150:
        request_number += 1
        lst = df.iloc[request_number].values
        lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)
        higherBuyQuantity = findhigherBuy(lst,lowestIndex)

        if toBuy:
            if buyCondition(lst):
                buyAmount = buyCost
                toBuy = 0
        else:
            if sellCondition(lst,buyAmount):
                profit += min(0.5,buyCost - buyAmount)
                toBuy = 1
                buyAmount = 0
            
    profit = profit - buyAmount
    return profit
