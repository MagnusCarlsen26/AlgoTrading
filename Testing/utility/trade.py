import numpy as np

def findLowestBuy(lst):
    nonzero_indices = np.nonzero(lst)[0] 
    if nonzero_indices.size > 0:  
        lowest_index = nonzero_indices[0] 
        return lowest_index, lst[lowest_index], (lowest_index + 1) / 2
    else:
        return -1, 0, 0 

def trade(item_path,df,stopLoss,bookprofit,buyCondition,sellCondition,buyDelay,sellDelay,prices,trades,toBuy=1,costPrice=0,profit=0,request_number=5,time=0):
    while request_number < len(df)-1-sellDelay:
        lst = df.iloc[request_number].values
        lst = np.array(lst[:len(lst)-2])
        lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)

        if toBuy:
            if request_number > len(df) - time*10:
                break
            buyQuantity = buyCondition(df,request_number,item_path)
            if buyQuantity:
                buyIndex = request_number
                lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number+buyDelay].values)
                costPrice = buyCost
                toBuy = 0
        else:
            if sellCondition(df,request_number,costPrice,bookprofit,stopLoss,item_path):
                lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number+sellDelay].values)
                if buyCost - costPrice > 0:
                    profit += (min(bookprofit,(buyCost-0.5)-costPrice) )*buyQuantity*0.8
                    # print(f"profit = {(min(bookprofit,(buyCost-0.5)-costPrice) )*buyQuantity}")
                    prices[str(costPrice)] += float(min(bookprofit,(buyCost-0.5)-costPrice))*buyQuantity*0.8
                else:
                    profit += max(-stopLoss,(buyCost-0.5) - costPrice)*buyQuantity
                    # print(f"Loss = {max(-stopLoss,(buyCost-0.5) - costPrice)*buyQuantity} ")
                    prices[str(costPrice)] += float(max(-stopLoss,(buyCost-0.5) - costPrice))*buyQuantity

                toBuy = 1
                costPrice = 0
        request_number += 1
    if costPrice != 0:
        print(f'Waste = {costPrice} , {item_path} , {buyIndex}')
    profit = profit - costPrice
    return profit
