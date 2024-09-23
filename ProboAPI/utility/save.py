import pandas as pd
import os
from datetime import datetime

def checkdir(folderName):
    if not ( os.path.exists(folderName) and os.path.isdir(folderName) ):
        os.makedirs(folderName)

def save(type,transposed_data,title,time,fileOrigin):
    today = datetime.today()
    date = today.strftime("%Y-%m-%d")
    folderName = title[-9:][:8].replace(':','-')[-9:][:8].replace(':','-') + " " + title.split()[5]
    folderName = fileOrigin + '/' +str(date) + '/' +folderName
    transposed_data['time'] = time 
    with open("logs/output.txt", "r") as file :
        try:
            bitcoinPrice = float(file.read().strip())
        except ValueError as e:
            print(f"save : error : {e}")
            return
        
    transposed_data["bitcoinPrice"] = bitcoinPrice
    transposed_data = {k: [v] for k, v in transposed_data.items()} 
    df = pd.DataFrame(transposed_data)
    try:
        df.to_csv(f'{date}/{folderName}/{type}.csv', mode='a', index=True, header=False)  
    except:
        checkdir(folderName)
        df.to_csv(f'{folderName}/{type}.csv', mode='a', index=True, header=False)  




