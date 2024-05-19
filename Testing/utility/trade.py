def findLowestBuy(lst):
    lowestIndex = -1
    for i in range(19):
        if lst[i] != 0:
            lowestIndex = i
            break
    return lowestIndex,lst[lowestIndex],(lowestIndex+1)/2


def trade(df,stopLoss,bookprofit,buyCondition,sellCondition,toBuy=1,buyAmount=0,profit=0,request_number=5):
    global total_profit
    while request_number < len(df)-150:
        request_number += 1
        lst = df.iloc[request_number].values
        lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)

        if toBuy:
            if buyCondition(df,request_number):
                lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number+4].values)
                buyAmount = buyCost
                toBuy = 0
        else:
            if sellCondition(df,request_number,buyAmount,bookprofit,stopLoss):
                lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number+4].values)
                if buyCost - buyAmount >0:
                    profit += 0.5
                elif buyCost - buyAmount <= -1:
                    profit += -1
                profit += min(0.5,buyCost - buyAmount)
                toBuy = 1
                buyAmount = 0
            
    profit = profit - buyAmount
    return profit
