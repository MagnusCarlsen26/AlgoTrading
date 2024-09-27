import pandas as pd
import os
import numpy as np

def clean(base_directory = '../Bitcoin'):
    directories_to_search = [base_directory]
    prices = [str(i/2) for i in range(1,20)]
    prices.append('Time')
    prices.append('bitcoinPrice')

    while directories_to_search:
        current_directory = directories_to_search.pop(0)  
        for item in os.listdir(current_directory):
            item_path = os.path.join(current_directory, item)

            if os.path.isdir(item_path):
                directories_to_search.append(item_path)  
            elif item.endswith('.csv'):

                print(item_path)
                df = pd.read_csv(item_path)
                if len(df.columns) == 22 :
                    del df[df.columns[0]]
                    df.columns = prices
                    def your_function(row):
                        start = row[0]
                        for i in range(1,len(row)-2):
                            row.iloc[i] -= start
                            start += row.iloc[i]
                        return row
                    df = df.apply(lambda row: your_function(row), axis=1)
                    df.to_csv(item_path,index=False)
                
clean()