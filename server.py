from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)


def save(type,data,title):
    i = 0.5
    d = {}
    while i<10:
        d[i] = 0
        i += 0.5
        
    for i in range(len(data)):
        if data[i]['price'] !=  0:
            d[data[i]['price']] = data[i]['quantity']
    transposed_data = {str(key): [value] for key, value in d.items()}
    
    title = 'new/' + title
    checkdir(title)
    transposed_data['time'] = time
    df = pd.DataFrame(transposed_data)
    df.to_csv(f'{title}/{type}.csv', mode='a', index=True, header=False)  # Append mode, no header

def checkdir(title):
    if not ( os.path.exists(title) and os.path.isdir(title) ):
        os.makedirs(title)

def strategy(type,data,title):
    i = 0.5
    d = {}
    while i<10:
        d[i] = 0
        i += 0.5
    print(data)
    for i in range(len(data)):
        if data[i]['price'] !=  0:
            d[data[i]['price']] = data[i]['quantity']
    transposed_data = {str(key): [value] for key, value in d.items()}

    lst = []
    for i in transposed_data.keys():
        lst.append(transposed_data[i][0])
    trade(lst)

def trade(lst):
    def findLowest(lst):
        lowestIndex = -1
        for i in range(19):
            if lst[i] != 0:
                lowestIndex = i
                break
        return lowestIndex,lst[lowestIndex],(lowestIndex+1)/2

    def findhigherBuy(lst):
    
        higherBuy = 0
        for i in range(lowestIndex+1,19):
            if lst[i] > 0:
                higherBuy += lst[i]
        return higherBuy

    ratio = 7

    lowestIndex,lowerBuy,buyCost = findLowest(lst)
    if lowestIndex == -1:
        return

    higherBuyQuantity = findhigherBuy(lst)
    if higherBuyQuantity == 0:
        return
    if higherBuyQuantity/lowerBuy > ratio:
        print('BUY',time,buyCost)
        return
        
@app.route('/', methods=['POST'])
def receive_data():
    try:
        global time
        data = request.json
        yes_data = data.get('yesData')
        no_data = data.get('noData')
        title = data.get('title')[-9:][:8].replace(':','-')
        time = data.get('currentTime')

        # strategy('yes',yes_data,title)
        # strategy('no',yes_data,title)
        save('yes',yes_data,title)
        save('no',no_data,title)

        return "Data received successfully", 200
    except Exception as e:
        print("Error processing data:", e)
        return "Internal server error", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
