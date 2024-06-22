from dotenv import load_dotenv
import os
from save import save
from time import gmtime, strftime
import time
import json
from datetime import datetime,timezone
import websocket
import threading
import subprocess
from api import buy,buyBook,cancel_order,sell,trade_status,getEventIds,getBuyPrice,collectBitcoinPrice,collectData

load_dotenv()

authorization_dummy = os.environ.get('Authorization_Dummy') 
authorization_real = os.environ.get('Authorization_Real')
url = 'https://prod.api.probo.in/api/'
with open('config.json','r') as f:
    config = json.load(f)
prevdict = []
currdict = []
prices = [str(i/2) for i in range(1,20)]


def buyAlgorithm( buyBook : dict ) -> int :
    global prevdict,currdict

    with open("output.txt", "r") as file :
        try:
            bitcoinPrice = float(file.read().strip())
        except ValueError as e:
            return 0
        
    buyBook['bitcoinPrice'] = bitcoinPrice
    currdict = buyBook.copy()
    if prevdict == [] :
        print("EMPTY")
        prevdict = currdict.copy()
        return
    
    # Assuming only 'YES' orderbook
    if  (currdict['bitcoinPrice'] - prevdict['bitcoinPrice']) != 0 :
        print(currdict['bitcoinPrice'] - prevdict['bitcoinPrice'])
    # print(prevdict)
    # print(currdict)
    # print()
    currPrice = getBuyPrice(currdict)
    for ignore in ignores:
        if ignore <= currPrice <= ignore + 2:
            return 0

    if currdict['bitcoinPrice'] - prevdict['bitcoinPrice'] >= bitcoinPriceDiff :
        prevdict = currdict.copy()
        return currPrice
    prevdict = currdict.copy()
    return 0

def sellAlgorithm( buyBook : dict , buyPrice : int ) -> bool :
    global prevdict,currdict
    with open("output.txt", "r") as file :
        try:
            bitcoinPrice = float(file.read().strip())
        except ValueError as e:
            print(f"save : error : {e}")
            return 0
    buyBook['bitcoinPrice'] = bitcoinPrice
    currdict = buyBook.copy()
    if prevdict == [] :
        print("EMPTY")
        prevdict = buyBook.copy()
        return
    

    if - ( currdict['bitcoinPrice'] - prevdict['bitcoinPrice'] ) > bitcoinPriceDiff:
        return True
    currPrice = getBuyPrice(currdict)
    if buyPrice - (currPrice - 0.5) >= stoploss :
        return True
    return False
    
def trade( topicId : list[int] ) : 
    try:
        while True:
            eventId = getEventIds([topicId])[0]
            isToBuy = True
            print(f"eventId = {eventId}")
            while True :
                d = buyBook(eventId)
                if d['buyData'] == {}:
                    break
                minutes = int(d['title'][-9:][:8].split()[0][-2:])
                now = datetime.now()
                current_minute = now.minute
                if current_minute >= minutes:
                    minutes = 60 + minutes
                if minutes - current_minute <= 2 :
                    print(minutes,current_minute)
                    break
                if isToBuy :
                    buy_price = buyAlgorithm(d['buyData'])
                    if buy_price:
                        print(f"Buying for {buy_price}...")
                        order_id = buy( eventId = eventId , buy_price = buy_price ,  yesno = 'yes' )
                        time.sleep(0.5)
                        status = trade_status(eventId=eventId , order_id=order_id)
                        if status == 'Pending' :
                            print("Order didn't match, cancelling it.")
                            while status != 'Cancelled':
                                cancel_order(eventId,order_id)
                                status = trade_status(eventId,order_id)
                            print("Order Cancelled")
                        elif status == 'Matched':
                            sell( min(buy_price + bookprofit,9.5) , order_id)
                            isToBuy = 0
                            print("Analyzing for selling...")
                        else:
                            print(f"STATUS = {status}.............")
                else :
                    if 'Exited' in trade_status(eventId,order_id):
                        profit = (trade_status(eventId,order_id).split()[-1])
                        print(f"Order sold, profit = {profit}")
                        isToBuy = 1
                        print("Analyzing to Buy...")
                        continue
                    if sellAlgorithm(d['buyData'],buy_price) :
                        cancel_order(eventId,order_id)
                        sell(0.5 , order_id)
                        time.sleep(0.5)
                        profit = (trade_status(eventId,order_id).split()[-1])
                        print(f"Order sold, profit = {profit}")
                        isToBuy = 1
                        print("Analyzing to Buy...")
                # time.sleep(5)
    except Exception as e:
        print("ERROR",e)
        print("Restarting Trade ...")
        trade(topicId)


bitcoinPriceDiff = 10
stoploss = 2
bookprofit = 2
ignores = [0,8.5]

thread1 = threading.Thread(target=collectBitcoinPrice, args=())
thread2 = threading.Thread(target=trade, args=([2449]))

thread1.start()
thread2.start()