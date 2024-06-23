import time
import threading
from typing import Literal
from utility.api import buyBook,getBuyPrice,collectBitcoinPrice
from utility.abort import abort
from utility.smartQuestionSelector import smartQuestionSelector
from utility.readBitcoinPrice import readBitcoinPrice
import logging
import traceback

prevBitcoinPrice = None
logging.basicConfig(filename='trade_log.txt', level=logging.DEBUG,filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def buyAlgorithm( buyBook : dict , sellBook  : dict ) -> int :

    diff = readBitcoinPrice()

    if diff >= 1 :
        currPrice = getBuyPrice( buyBook )
        factor = 1
    elif diff <= -1:
        currPrice = getBuyPrice( sellBook )
        factor = -1
    else:
        return 0
    for ignore in ignores:
        if ignore <= currPrice <= ignore + 2:
            return 0
    if abs(diff) >= 5 :
        logging.debug(f"TRADE SHOULD HAPPEN difference = {diff}")
    if factor*diff >= bitcoinPriceDiff :
        print(f"Difference = {diff}")
        return factor*currPrice
    return 0

def sellAlgorithm( buyBook : dict , sellBook : dict ,buyPrice : int ,orderType : Literal['yes','no']) -> bool :
  
    diff = readBitcoinPrice()
    
    if orderType == 'yes' :
        currPrice = getBuyPrice(buyBook)
        factor = -1
    else:
        currPrice = getBuyPrice(sellBook)
        factor = 1
    
    if factor*diff > bitcoinPriceDiff:
        print(f"Difference = {diff}")
        print(f"Profit = {currPrice - buyPrice}. Sold becuase of diff.")
        return True
    if buyPrice - (currPrice - 0.5) >= stoploss :
        print(f"Selling for {currPrice - 0.5}")
        print(f"Profit = {(currPrice - 0.5) - buyPrice}. Sold becuase of stoploss.")
        return True
    if (currPrice - 0.5) - buyPrice >= bookprofit :
        print(f"Selling for {currPrice - 0.5}")
        print(f"Profit = {(currPrice - 0.5) - buyPrice}. Sold because of bookprofit.") 
        return True
    return False    

def trade( topicId : list[int] ) : 
    while True :
        with open("output.txt") as f:
            print(f.read(),'f')
            if f.read() != "":
                break
        time.sleep(0.5)
    try:
         while True:
            eventId = smartQuestionSelector(topicId)
            isToBuy = True
            d = buyBook(eventId)
            print(f"Question : {d['title']}")
            while True :
                d = buyBook(eventId)
                if abort(d['title'],isToBuy) :
                    break
                if isToBuy:
                    buy_price = buyAlgorithm(d['buyData'],d['sellData'])
                    if buy_price != 0:
                        orderType = 'yes' if buy_price > 0 else 'no'
                        buy_price = abs(buy_price)
                        print(f"Buying {orderType} for {buy_price}...")
                        time.sleep(0.2)
                        isToBuy = False
                        print("Analyzing for selling...")
                else :
                    if sellAlgorithm(d['buyData'],d['sellData'],buy_price,orderType) :
                        time.sleep(0.5)
                        isToBuy = True
                        print("Analyzing to Buy...")
                # time.sleep(5)
    except Exception as e:
        print(f"ERROR {e}")
        traceback.print_exc() 
        # trade(topicId)


bitcoinPriceDiff = 1
stoploss = 1.5
bookprofit = 1.5
ignores = [0,8]

thread1 = threading.Thread(target=collectBitcoinPrice, args=())
thread2 = threading.Thread(target=trade, args=([2449]))

thread1.start()
thread2.start()