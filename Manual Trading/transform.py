from datetime import datetime
import pandas as pd
def transform(data):

    cum_sum = 0
    for i in range(1,20):
        x = data[str(i/2)]
        data[str(i/2)] -= cum_sum
        cum_sum += data[str(i/2)]
    return data