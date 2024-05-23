from utility.trade import trade
from utility.test import test
from utility.findLowestBuy import findLowestBuy
from utility.findhigherBuy  import findhigherBuy
import matplotlib.pyplot as plt
import os
import pandas as pd

params = [0.75,1,1.25]
importance = 0
profit = []
loss = []

def buyCondition(df,request_number):
    lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number].values)
    if lowestIndex == -1 :
        buyCost = 10
    if len(df)//(3*divideRatio) <= request_number :
        importance += buyCost*params[0]
    elif len(df)//(3*divideRatio) < request_number <= len(df)//(divideRatio) :
        importance += buyCost*params[1]
    elif request_number < len(df)//(divideRatio) :
        importance += buyCost*params[2]
    elif request_number == len(df)//(divideRatio) :
        importance = importance // (len(df)//divideRatio) 
        if importance > cutoff :
            lowestIndex,lowerBuy,cp = findLowestBuy(df.iloc[len(df)//2].values)
            return 1
    return 0
        


def trade(df):
    global importance
    request_number = 0
    while request_number < len(df) - 2:

        lowestIndex,lowerBuy,buyCost = findLowestBuy(df.iloc[request_number].values)
        if lowestIndex == -1 :
            buyCost = 10
        if len(df)//6 <= request_number :
            importance += buyCost*params[0]
        elif len(df)//6 < request_number <= len(df)//3 :
            importance += buyCost*params[1]
        elif request_number < len(df)//2:
            importance += buyCost*params[2]
        else:
            break
        request_number += 1
    importance = importance // (len(df)//2)
    if importance > cutoff :
        lowestIndex,lowerBuy,cp = findLowestBuy(df.iloc[len(df)//2].values)
        if lowestIndex != -1 :
            lowestIndex,lowerBuy,sp = findLowestBuy(df.iloc[len(df)-1].values)
            if lowestIndex == -1 :
                profit.append(cp)
                return 10 - cp
            else:
                loss.append(cp)
                return -cp    
    return 0

p = []
for cutoff in range(9,10):
    p.append(test())
    plt.hist(profit, bins=19, color='green', alpha=0.8)  # Adjust bins as needed

    # Add labels and title (optional)
    plt.xlabel('CP')
    plt.ylabel('Frequency')
    plt.title('Profit')

    # Show the plot
    plt.show()
    plt.hist(loss, bins=19, color='red', alpha=0.8)  # Adjust bins as needed
    plt.xlabel('CP')
    plt.ylabel('Frequency')
    plt.title('Loss')
    plt.show()

plt.plot(p)
plt.show()