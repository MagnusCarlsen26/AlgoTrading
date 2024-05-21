from datetime import datetime
import pandas as pd
def transform(type,data,title,time):
    today = datetime.today()
    date = today.strftime("%Y-%m-%d")

    i = 0.5
    d = {}
    while i<10:
        d[i] = 0
        i += 0.5
    for i in range(len(data)):
        if data[i]['price'] !=  0:
            d[data[i]['price']] = data[i]['quantity']
    transposed_data = {str(key): [value] for key, value in d.items()}
    
    title = 'data/' +str(date) + '/' +title
    transposed_data['time'] = time
    df = pd.DataFrame(transposed_data)
    
    return df