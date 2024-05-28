import numpy as np

def findLowestBuy(lst):
    nonzero_indices = np.nonzero(lst)[0] 
    if nonzero_indices.size > 0:  
        lowest_index = nonzero_indices[0] 
        return lowest_index, lst[lowest_index], (lowest_index + 1) / 2
    else:
        return -1, 0, 0 

def trade(item_path,df,stopLoss,bookprofit,buyCondition,sellCondition,buyDelay,sellDelay,toBuy=1,costPrice=0,profit=0,request_number=5,time=120):
    global total_profit
    madeProfit = 0
    madeLoss = 0
    # print(item_path)
    while request_number < len(df)-1-sellDelay:
        request_number += 1
        lst = df.iloc[request_number].values
        lst = np.array(lst[:len(lst)-1])
        lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)

        if toBuy:
            if request_number > len(df) - time*10:
                break
            if buyCondition(df,request_number):
                # print()
                # print(f'prev    {df.iloc[request_number -10].values}')
                # print(f'Buying  {lst}')
                lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number+buyDelay].values)
                costPrice = buyCost
                toBuy = 0
        else:
            if sellCondition(df,request_number,costPrice,bookprofit,stopLoss):
                lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number+sellDelay].values)
                if buyCost - costPrice > 0:
                    profit += min(bookprofit,(buyCost-0.5)-costPrice)
                else:
                    profit += max(-stopLoss,(buyCost-0.5) - costPrice)
                toBuy = 1
                costPrice = 0
    # print(f'Made Profit = {madeProfit} , Made Loss = {madeLoss}')
    # print('----------------------------------------------')
    profit = profit - costPrice
    return profit
