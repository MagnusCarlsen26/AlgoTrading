import pandas as pd
import os
from datetime import datetime

def checkdir(title):
    if not ( os.path.exists(title) and os.path.isdir(title) ):
        os.makedirs(title)

def save(type,transposed_data,title,time):
    today = datetime.today()
    date = today.strftime("%Y-%m-%d")

    title = 'Bitcoin/' +str(date) + '/' +title
    transposed_data['time'] = time
    transposed_data = {k: [v] for k, v in transposed_data.items()} 

    df = pd.DataFrame(transposed_data)

    try:
        df.to_csv(f'{date}/{title}/{type}.csv', mode='a', index=True, header=False)  
    except:
        checkdir(title)
        df.to_csv(f'{title}/{type}.csv', mode='a', index=True, header=False)  




