import pandas as pd
import os
from findLowestBuy import findLowestBuy
from  findhigherBuy import findhigherBuy
import numpy as np
def test(strategy,stopLoss,bookprofit,buyCondition,sellCondition,buyDelay,sellDelay,base_directory = '../../Data Collection/preProcessedData'):
    directories_to_search = [base_directory]  
    profit = 0
    a = 0
    while directories_to_search:
        current_directory = directories_to_search.pop(0)  
        for item in os.listdir(current_directory):
            item_path = os.path.join(current_directory, item)

            if os.path.isdir(item_path):
                directories_to_search.append(item_path)  
            elif item.endswith('.csv'):
                print(item_path)
                df = pd.read_csv(item_path)
                newdf = { 'buyCost':[],'lowerBuy':[],'lowestIndex' : [] , 'findhigherBuy':[] }
                for index,row in df.iterrows():
                    row = np.array(row[:len(row)-1])
                    lowestIndex,lowerBuy,buyCost = findLowestBuy(row)
                    higherBuyQuantity = findhigherBuy(row,lowestIndex)
                    newdf['lowestIndex'].append(lowestIndex)
                    newdf['buyCost'].append(buyCost)
                    newdf['lowerBuy'].append(lowerBuy)
                    newdf['findhigherBuy'].append(higherBuyQuantity)
                df = pd.DataFrame(newdf) 
                df.to_csv(item_path,index=False)
    print(f'Total Profit = {profit}')
    print(a)
    return profit

test(1,2,3,4,5,6,7)