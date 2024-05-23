from datetime import datetime
import pandas as pd
def transform(type,data,title):

    i = 0.5
    d = {}
    while i<10:
        d[i] = 0
        i += 0.5
    for i in range(len(data)):
        if data[i]['price'] !=  0:
            d[data[i]['price']] = data[i]['quantity']
    transposed_data = {str(key): [value] for key, value in d.items()}
    
    df = pd.DataFrame(transposed_data)
    
    return df