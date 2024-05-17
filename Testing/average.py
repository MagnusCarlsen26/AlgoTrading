from utility.trade import trade
from utility.test import test
from utility.findLowestBuy import findLowestBuy
from utility.findhigherBuy  import findhigherBuy

def sellCondition(lst,buyAmount,bookprofit=0.5,stopLoss=1):
    lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)
    if buyCost-buyAmount>=bookprofit or buyAmount - buyCost >= stopLoss:
        return 1
    return 0

def buyCondition(lst,ratio=3):
    lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)
    higherBuyQuantity = findhigherBuy(lst,lowestIndex)
    if lowestIndex == -1 or higherBuyQuantity == 0:
        return 0
    elif higherBuyQuantity/lowerBuy > ratio:
        return 1
    return 0

test(trade,stopLoss=1,bookprofit=0.5,buyCondition = buyCondition,sellCondition = sellCondition)
