from utility.trade import trade
from utility.test import test
from utility.findLowestBuy import findLowestBuy
from utility.findhigherBuy  import findhigherBuy
import matplotlib.pyplot as plt
import numpy as np

def sellCondition(df,request_number,buyAmount,bookprofit=0.5,stopLoss=1):
    return 1

def buyCondition(df,request_number):
    currlst = df.iloc[request_number].values
    prevlst = df.iloc[request_number-1].values
    currlowestIndex,currlowerBuy,currbuyCost = findLowestBuy(np.array(currlst[:len(currlst)-1]))
    prevlowestIndex,prevlowerBuy,prevbuyCost = findLowestBuy(np.array(prevlst[:len(prevlst)-1]))

    higherBuyQuantity = findhigherBuy(np.array(currlst[:len(currlst)-1]),currlowestIndex)
    if currlowestIndex == -1 :
        return 0
    elif ignore<=currbuyCost<=ignore+2:
        return 0
    elif higherBuyQuantity/currlowerBuy > ratio:
        if currbuyCost <= prevbuyCost :
            # print(prevlowerBuy,currlowerBuy)
            if prevlowerBuy - currlowerBuy > cutoff:
                return 1
    return 0

profit = []
ignore = 9
for ratio in range(2,20,2):
    print(f'Ratio = {ratio} -------------------------------------------')
    for cutoff in range(100,2000,300):
        profit.append(test(trade,stopLoss=1,bookprofit=0.5,buyCondition = buyCondition,sellCondition = sellCondition,buyDelay=0,sellDelay=0))

plt.plot(cutoff , profit)
plt.xlabel('Cutoff')
plt.ylabel('Profit')
plt.show()