import pandas as pd
import os
import numpy as np

def test(strategy,stopLoss,bookprofit,buyCondition,sellCondition,buyDelay,sellDelay,base_directory = '../Data Collection/data'):
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
                df = pd.read_csv(item_path)
                x = strategy(item_path,df,stopLoss,bookprofit,buyCondition,sellCondition,buyDelay,sellDelay)
                print(f'Overall Profit = {x}')
                profit += x
    print(f'Total Profit = {profit}')
    return profit
