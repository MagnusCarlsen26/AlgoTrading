from utility.trade import trade
from utility.test import test
from utility.findLowestBuy import findLowestBuy
from utility.findhigherBuy  import findhigherBuy
import matplotlib.pyplot as plt
import numpy as np

def sellCondition(df,request_number,costPrice,bookprofit=0.5,stopLoss=1,item_path=""):
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
            print(f"Selling at {buyCost-0.5} {request_number} yes")
            return 1
        else :
            return 0
    else:
        if ( currlst[-1] - prevlst[-1] ) > bitcoinPriceDiff*1 :
            print(f"Selling at {buyCost-0.5} {request_number} no")
            return 1
        else :
            return 0

def buyCondition(df,request_number,item_path):
    target = float(item_path[-16:][:8])
    currlst = df.iloc[request_number].values
    prevlst = df.iloc[request_number - 1].values
    global trades
    # if abs(target - currlst[-1]) > bitcoincutoff :
    #     return 0
    lowestIndex,lowerBuy,buyCost = findLowestBuy(currlst)
    for ignore in ignores:
        if ignore <= buyCost <= ignore + 2:
            return 0
    if 'yes.csv' in item_path : 
        if ( currlst[-1] - prevlst[-1] ) > bitcoinPriceDiff :
            trades += 1
            print(f"Buying at {buyCost} ,{request_number} yes")
            return 1
        else :
            return 0
    else:
        if - ( currlst[-1] - prevlst[-1] ) > bitcoinPriceDiff :
            trades += 1
            print(f"Buying at {buyCost} ,{request_number} no")
            return 1
        else :
            return 0

bitcoinPriceDiff = 10
profit = []
xaxis=  []
ignores = [0,9]

prices = { str(i/2):0 for i in range(1,21) }
trades = 0
trades =0
for bitcoincutoff in range(10,20,10):
    profit.append(test(trade,stopLoss=1.5,bookprofit=1.5,buyCondition = buyCondition,sellCondition = sellCondition,buyDelay=0,sellDelay=0,prices = prices ,trades = trades,base_directory='../ProboAPI/Bitcoin'))
    xaxis.append(bitcoincutoff)

plt.plot(xaxis, profit, marker='o', linestyle='--', color='skyblue')  # Added style options

plt.xlabel('bitcoinPriceDiff')
plt.ylabel('Profit')

plt.grid(axis='y', linestyle='-') 

plt.show()

print(trades)