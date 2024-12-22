import pandas as pd
import os

def checkdir(folderName):
    if not ( os.path.exists(folderName) and os.path.isdir(folderName) ):
        os.makedirs(folderName)

def save(type,d,folderName):

    transposed_data = {k: [v] for k, v in d.items()} 
    df = pd.DataFrame(transposed_data)
    try:
        df.to_csv(f'{folderName}/{type}.csv', mode='a', index=True, header=False)  
    except:
        checkdir(folderName)
        df.to_csv(f'{folderName}/{type}.csv', mode='a', index=True, header=False)  




