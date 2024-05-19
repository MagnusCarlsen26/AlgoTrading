from utility.trade import trade
from utility.test import test
from utility.findLowestBuy import findLowestBuy
from utility.findhigherBuy  import findhigherBuy
import matplotlib.pyplot as plt

def sellCondition(df,request_number,buyAmount,bookprofit=0.5,stopLoss=1):
    
    lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number].values)
    if buyCost-buyAmount>=bookprofit or buyAmount - buyCost >= stopLoss:
        return 1
    return 0

def buyCondition(df,request_number):
    i = -5
    while i<0:
        i += 1
        lst = df.iloc[request_number+i].values
        lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)
        higherBuyQuantity = findhigherBuy(lst,lowestIndex)
        if lowestIndex == -1 or higherBuyQuantity == 0:
            return 0
        elif higherBuyQuantity/lowerBuy > ratio:
            continue
        return 0
    return 1

l = []
# ratio = 18
for ratio in range(4,50,7):
    profit = test(trade,stopLoss=1,bookprofit=0.5,buyCondition = buyCondition,sellCondition = sellCondition)
    l.append(profit)
# for stopLoss in range(1,6):
# profit = test(trade,stopLoss=1,bookprofit=0.5,buyCondition = buyCondition,sellCondition = sellCondition)
#     l.append(profit)
plt.plot(range(1,len(l)+1),l) # Use range(len(values)) for x-axis

plt.xlabel("Index")
plt.ylabel("Profit")
plt.title("Line Chart")

plt.show()