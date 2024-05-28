from utility.findLowestBuy import findLowestBuy
from utility.findhigherBuy  import findhigherBuy
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
def test(stopLoss,bookprofit,base_directory = '../Data Collection/analysis'):
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
                strategy(df,stopLoss,bookprofit)
                a += 1
                print(a)
    return 

def strategy(df,stopLoss,bookprofit):
    request_number = 0

    while request_number < len(df) - 1 :
        currlst = df.iloc[request_number].values
        currlst = np.array(currlst[:len(currlst)-1])
        currlowestIndex,currlowerBuy,currbuyCost = findLowestBuy(currlst)
        original_request_number = request_number

        while request_number < len(df) - 1 :
            nextlst = df.iloc[request_number].values
            nextlst = np.array(nextlst[:len(nextlst)-1])
            nextowestIndex,nextowerBuy,nextbuyCost = findLowestBuy(nextlst)
            request_number += 1

            if nextbuyCost - currbuyCost > bookprofit :
                with open('profit.csv', 'a') as f:
                    f.write('buy  ')  # No comma after 'buy'
                    for value in currlst:  
                        f.write(f"{value} ")  # Write each value with a space
                    
                    for fuck in range(original_request_number+1,request_number):
                        intrlst = df.iloc[fuck].values
                        intrlst = np.array(intrlst[:len(intrlst)-1])
                        f.write('\nintr ')
                        for value in intrlst:
                            f.write(f'{value} ')

                    f.write('\nsell ')  # No comma after 'selln'
                    for value in nextlst:
                        f.write(f"{value} ")
                    f.write('\n')
                    f.write('\n')
                break

            elif nextbuyCost - currbuyCost <= -stopLoss:
                with open('loss.csv', 'a') as f:
                    f.write('buy  ')  # No comma after 'buy'
                    for value in currlst:  
                        f.write(f"{value} ")  # Write each value with a space
                    
                    for fuck in range(original_request_number+1,request_number):
                        intrlst = df.iloc[fuck].values
                        intrlst = np.array(intrlst[:len(intrlst)-1])
                        f.write('\nintr ')
                        for value in intrlst:
                            f.write(f'{value} ')

                    f.write('\nsell ')  # No comma after 'selln'
                    for value in nextlst:
                        f.write(f"{value} ")
                    f.write('\n')
                    f.write('\n')

                break
test(1,0.5)