def findLowestBuy(lst):
    lowestIndex = -1
    for i in range(19):
        if lst[i] != 0:
            lowestIndex = i
            break
    return lowestIndex,lst[lowestIndex],(lowestIndex+1)/2


def trade(df,stopLoss,bookprofit,buyCondition,sellCondition,buyDelay,sellDelay,toBuy=1,buyAmount=0,profit=0,request_number=5):
    global total_profit
    while request_number < len(df)-1:
        request_number += 1
        lst = df.iloc[request_number].values
        lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)

        if toBuy:
            if request_number > len(df) - 600:
                break
            if buyCondition(df,request_number):
                lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number+buyDelay].values)
                buyAmount = buyCost
                toBuy = 0
        else:
            if sellCondition(df,request_number,buyAmount,bookprofit,stopLoss):
                lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number+sellDelay].values)
                if buyCost - buyAmount > 0:
                    profit += 0.5
                elif buyCost - buyAmount <= -stopLoss:
                    profit += -stopLoss
                # profit += min(0.5,buyCost - buyAmount)
                toBuy = 1
                buyAmount = 0
            
    profit = profit - buyAmount
    return profit
