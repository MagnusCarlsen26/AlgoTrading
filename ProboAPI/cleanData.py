import pandas as pd
import os
import numpy as np

def clean(base_directory = './Bitcoin'):
    directories_to_search = [base_directory]
    while directories_to_search:
        current_directory = directories_to_search.pop(0)  
        for item in os.listdir(current_directory):
            item_path = os.path.join(current_directory, item)

            if os.path.isdir(item_path):
                directories_to_search.append(item_path)  
            elif item.endswith('.csv'):

                print(item_path)
                df = pd.read_csv(item_path)

                def your_function(row):
                    start = row[0]
                    for i in range(len(row)-1):
                        row[i] -= start
                        start += row[i]
                    return row
                df = df.apply(lambda row: your_function(row), axis=1)
                df.to_csv(item_path,index=False)
clean()