import pandas as pd
import os
import numpy as np

def findLowestBuy(lst):
    nonzero_indices = np.nonzero(lst)[0] 
    if nonzero_indices.size > 0:  
        lowest_index = nonzero_indices[0] 
        return lowest_index, lst[lowest_index], (lowest_index + 1) / 2
    else:
        return -1, 0, 10
notWorking = 0
def arbitage(item_path) :
    global notWorking
    print(item_path)
    yesdf = pd.read_csv(f"{item_path}/yes.csv")
    nodf = pd.read_csv(f"{item_path}/no.csv")
    
    request_number = 0
    profit = 0  
    isBuy = True
    count = 0
    while request_number < (min(len(yesdf),len(nodf))) :
        yeslst = yesdf.iloc[request_number].values
        nolst = nodf.iloc[request_number].values

        yeslst = np.array(yeslst[:len(yeslst)-2])
        nolst = np.array(nolst[:len(nolst)-2])

        yeslowestIndex,yeslowerBuy,yesbuyCost = findLowestBuy(yeslst)        
        nolowestIndex,nolowerBuy,nobuyCost = findLowestBuy(nolst)

        import random
        if isBuy :
            choice = ['yes','no']
            choice = choice[random.randint(0,1)]
            if choice == 'yes' :
                buyCost = yesbuyCost
                toBuy = 'no'
                isBuy = False
            else :
                buyCost = nobuyCost
                toBuy = 'yes'
                isBuy = False
        else :
            if toBuy == 'yes' :
                if yesbuyCost + buyCost < 10 :
                    count += 1
                    return 10 - (yesbuyCost + buyCost)
                    break
            else :
                if nobuyCost + buyCost < 10 :
                    count  += 1
                    return 10 - (nobuyCost + buyCost)
                    break
        request_number += 1
    return 0

def test(base_directory = '../ProboAPI/Bitcoin'):
    directories_to_search = [base_directory]  
    profit = 0
    done = []
    while directories_to_search:
        current_directory = directories_to_search.pop(0)  
        for item in os.listdir(current_directory):
            item_path = os.path.join(current_directory, item)

            if os.path.isdir(item_path):
                directories_to_search.append(item_path)  
            elif item.endswith('.csv'):
                # print(f'Overall Profit = {x}')
                folderName = item_path[:-4]
                if folderName[-1] == 's':
                    folderName = folderName[:-3]
                else:
                    folderName = folderName[:-2]
                if folderName not in done :
                    profit += arbitage(folderName)
                    done.append(folderName)
    print(f'Total Profit = {profit}')
    print(len(done))
    return profit

test()
print(notWorking)