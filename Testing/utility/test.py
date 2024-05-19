import pandas as pd
import os

def test(strategy,stopLoss,bookprofit,buyCondition,sellCondition,base_directory = '../Data Collection/data'):
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
                x = strategy(df,stopLoss,bookprofit,buyCondition,sellCondition)
                # print(f'Overall Profit = {x}')
                profit += x
                a += 1
    print(f'Total Profit = {profit}')
    print(a)
    return profit