from utility.trade import trade
from utility.test import test
from utility.findLowestBuy import findLowestBuy
from utility.findhigherBuy  import findhigherBuy
import matplotlib.pyplot as plt
import numpy as np

def sellCondition(df,request_number,buyAmount,bookprofit=0.5,stopLoss=1):
    return 1

def buyCondition(df,request_number):
    global preCheck
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
        elif ignore<=buyCost<=ignore+2:
            return 0
        elif higherBuyQuantity/lowerBuy > ratio:
            continue
        return 0
    return 1

ignore = 9
ratio = 112
profit = []
ratios = []
# for ratio in range(100,120,2):
profit.append(test(trade,stopLoss=1,bookprofit=0.5,buyCondition = buyCondition,sellCondition = sellCondition,buyDelay=0,sellDelay=0))
    # ratios.append(ratio)
    # print(profit)
plt.plot(ratios,profit)
plt.xlabel('ratios')
plt.ylabel('profit')
plt.show()