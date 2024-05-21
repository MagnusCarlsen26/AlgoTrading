import pandas as pd
import os
from datetime import datetime


def checkdir(title):
    if not ( os.path.exists(title) and os.path.isdir(title) ):
        os.makedirs(title)

def save(type,data,title,time):
    today = datetime.today()
    date = today.strftime("%Y-%m-%d")

    i = 0.5
    d = {}
    while i<10:
        d[i] = 0
        i += 0.5
    print(data)
    print()
    for i in range(len(data)):
        if data[i]['price'] !=  0:
            d[data[i]['price']] = data[i]['quantity']
    transposed_data = {str(key): [value] for key, value in d.items()}
    
    title = 'data/' +str(date) + '/' +title
    transposed_data['time'] = time
    df = pd.DataFrame(transposed_data)

    try:
        df.to_csv(f'{date}/{title}/{type}.csv', mode='a', index=True, header=False)  
    except:
        checkdir(title)
        df.to_csv(f'{title}/{type}.csv', mode='a', index=True, header=False)  




