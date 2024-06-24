from utility.trade import trade
from utility.test import test
from utility.findLowestBuy import findLowestBuy
from utility.findhigherBuy  import findhigherBuy
import matplotlib.pyplot as plt
import numpy as np

def sellCondition(df,request_number,costPrice,bookprofit,stopLoss,item_path):
    lst = df.iloc[request_number].values
    lst = np.array(lst[:len(lst)-2])
    lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)

    if buyCost - costPrice > bookprofit:
        return 1
    elif buyCost - costPrice <= -stopLoss :
        return 1
    
    currlst = df.iloc[request_number].values
    prevlst = df.iloc[request_number - 1].values
    if 'yes.csv' in item_path :
        if - ( currlst[-1] - prevlst[-1] ) > bitcoinPriceDiff*1 :
            return 1
        else :
            if - ( currlst[-1] - priceDuringBuying ) > bitcoinPriceDiff*multiplier :
                return 1
            return 0
    else:
        if ( currlst[-1] - prevlst[-1] ) > bitcoinPriceDiff*1 :
            return 1
        else :
            if ( currlst[-1] - priceDuringBuying ) > bitcoinPriceDiff :
                return 1
            return 0

def buyCondition(df,request_number,item_path):
    global trades,priceDuringBuying
    currlst = df.iloc[request_number].values
    prevlst = df.iloc[request_number - 1].values
    lowestIndex,lowerBuy,buyCost = findLowestBuy(currlst)

    for ignore in ignores:
        if ignore <= buyCost <= ignore + 2:
            return 0
        
    if 'yes.csv' in item_path :
        if ( currlst[-1] - prevlst[-1] ) > bitcoinPriceDiff :
            trades += 1
            priceDuringBuying = currlst[-1]
            return ( currlst[-1] - prevlst[-1] ) // bitcoinPriceDiff 
        else :
            return 0
    else:
        if - ( currlst[-1] - prevlst[-1] ) > bitcoinPriceDiff :
            trades += 1
            priceDuringBuying = currlst[-1]
            return - ( currlst[-1] - prevlst[-1] ) // bitcoinPriceDiff 
        else :
            return 0

# PARAMETERS
bitcoinPriceDiff = 10
ignores = [-1,9]
multiplier = 2

# CONSTANTS
profit = []
prices = { str(i/2):0 for i in range(1,21) }
trades = 0
xaxis=  []
trades = 0
priceDuringBuying = None

for p in range(3,4):
    profit.append(test(trade,stopLoss=2,bookprofit=2,buyCondition = buyCondition,sellCondition = sellCondition,buyDelay=0,sellDelay=0,prices = prices ,trades = trades,base_directory='../ProboAPI/Bitcoin'))
    xaxis.append(bitcoinPriceDiff)

plt.plot(xaxis, profit, marker='o', linestyle='--', color='skyblue')

plt.xlabel('Multiplier')
plt.ylabel('Profit')

plt.grid(axis='y', linestyle='-') 

plt.show()

print(f"Total trades = {trades}")
print(f"Distribution = ")
print(prices)
