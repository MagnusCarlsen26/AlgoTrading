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
    global preCheck
    prevCheck = 5
    i = -prevCheck
    while i<0:
        i += 1
        lst = df.iloc[request_number+i].values
        lowestIndex,lowerBuy,buyCost = findLowestBuy(lst)
        higherBuyQuantity = findhigherBuy(lst,lowestIndex)
        if lowestIndex == -1 or higherBuyQuantity == 0:
            return 0
        elif ignore<=buyCost<=ignore+2:
            return 0
        elif higherBuyQuantity/lowerBuy > ratio:
            continue
        return 0
    return 1

l = []
for ignore in range(0,10,2):
    x = []
    for ratio in range(1,25,5):
        profit = test(trade,stopLoss=1,bookprofit=0.5,buyCondition = buyCondition,sellCondition = sellCondition,buyDelay=5,sellDelay=5)
        x.append(profit)
    l.append(x)
    
xaxis = list(range(len(l[0])))  # [0, 1, 2, 3] in this example
plt.figure(figsize=(10, 6))  # Optional: set figure size

# Plot each line
for i, row in enumerate(l):
    plt.plot(xaxis, row, label=f"Line {i+1}")

plt.xlabel("X-axis Label")
plt.ylabel("Y-axis Label")
plt.title("Multiple Line Chart from 2D Array")
plt.grid(True)
plt.legend()

plt.show()