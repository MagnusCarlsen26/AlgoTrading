from utility.trade import trade
from utility.test import test
from utility.findLowestBuy import findLowestBuy
from utility.findhigherBuy  import findhigherBuy
import matplotlib.pyplot as plt
import numpy as np

def sellCondition(df,request_number,costPrice,bookprofit=0.5,stopLoss=1):
    lst = df.iloc[request_number].values
    lst = np.array(lst[:len(lst)-1])
    lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)

    if buyCost - costPrice > bookprofit:
        return 1
    elif buyCost - costPrice <= -stopLoss :
        return 1
    return 0

def buyCondition(df,request_number):
    prevCheck = 5
    i = -prevCheck
    prevbuyCost = 0
    prevLowerbuy = 0
    while i<0:
        i += 1
        lst = df.iloc[request_number+i].values
        lst = np.array(lst[:len(lst)-1])
        lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)
        higherBuyQuantity = findhigherBuy(lst,lowestIndex)
        if lowestIndex == -1 :
            return 0
        for ig in ignore:
            if ig<=buyCost<=ig+2:
                return 0
        if higherBuyQuantity/lowerBuy > ratio:
            continue
        return 0
    return 1

ignore = [0,9]
ratio = 10
profit = []
ratios = []
# for ratio in range(100,120,2):
profit.append(test(trade,stopLoss=2,bookprofit=2,buyCondition = buyCondition,sellCondition = sellCondition,buyDelay=0,sellDelay=0))
    # ratios.append(ratio)2
    # print(profit)
# plt.plot(ratios,profit)
# plt.xlabel('ratios')
# plt.ylabel('profit')
# plt.show()