import time
import threading
from typing import Literal
from utility.api import buyBook,getBuyPrice,collectBitcoinPriceFromProbo
from utility.abort import abort
from utility.smartQuestionSelector import smartQuestionSelector
from utility.readBitcoinPrice import readBitcoinPrice
import logging
import traceback
from utility.sendEmail import sendEmail

logging.basicConfig(
    filename='logs/trade_log.txt', 
    level=logging.INFO,
    filemode='w', 
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

prevBitcoinPrice = 0

def buyAlgorithm( buyBook : dict , sellBook  : dict ) -> int :
    global prevBitcoinPrice
    currBitcoinPrice = readBitcoinPrice()
    if prevBitcoinPrice != 0 :
        diff = currBitcoinPrice - prevBitcoinPrice
    else :
        prevBitcoinPrice = currBitcoinPrice
        return 0
    prevBitcoinPrice = currBitcoinPrice
    if diff >= 1 :
        currPrice = getBuyPrice( buyBook )
        factor = 1
    elif diff <= -1:
        currPrice = getBuyPrice( sellBook )
        factor = -1
    else:
        return 0
    print(diff)
    
    for ignore in ignores:
        if ignore <= currPrice <= ignore + 2:
            return 0

    if factor*diff >= bitcoinPriceDiff :
        logging.info(f"Difference = {diff}")
        return factor*currPrice
    return 0

def sellAlgorithm( buyBook : dict , sellBook : dict ,buyPrice : int ,orderType : Literal['yes','no']) -> bool :
    global prevBitcoinPrice
    currBitcoinPrice = readBitcoinPrice()
    if prevBitcoinPrice != 0 :
        diff = currBitcoinPrice - prevBitcoinPrice
    else:
        prevBitcoinPrice = currBitcoinPrice
        return 0
    prevBitcoinPrice = currBitcoinPrice
    if orderType == 'yes' :
        currPrice = getBuyPrice(buyBook)
        factor = -1
    else:
        currPrice = getBuyPrice(sellBook)
        factor = 1
    
    if factor*diff > bitcoinPriceDiff:
        logging.info(f"Selling for {currPrice - 0.5}")
        logging.info(f"Delta = {(currPrice - 0.5) - buyPrice}. Sold because of difference = {diff}.")
        return True
    if buyPrice - (currPrice - 0.5) >= stoploss :
        logging.info(f"Selling for {currPrice - 0.5}")
        logging.info(f"Loss = {(currPrice - 0.5) - buyPrice}. Sold becuase of stoploss.")
        return True
    if (currPrice - 0.5) - buyPrice >= bookprofit :
        logging.info(f"Selling for {currPrice - 0.5}")
        logging.info(f"Profit = {(currPrice - 0.5) - buyPrice}. Sold because of bookprofit.") 
        return True
    return False    

def trade( topicId : list[int] ) : 
    while True :
        with open("logs/output.txt") as f:
            if f.read() != "":
                break
        time.sleep(0.5)
    try:
         while True:
            eventId = smartQuestionSelector(topicId)
            isToBuy = True
            d = buyBook(eventId)
            logging.info(f"Question : {d['title']}")
            while True :
                d = buyBook(eventId)
                # if abort(d['title'],isToBuy) :
                #     break
                if isToBuy:
                    buy_price = buyAlgorithm(d['buyData'],d['sellData'])
                    if buy_price != 0:
                        orderType = 'yes' if buy_price > 0 else 'no'
                        buy_price = abs(buy_price)
                        logging.info(f"Buying {orderType} for {buy_price}...")
                        time.sleep(0.2)
                        isToBuy = False
                        logging.info("Analyzing for selling...")
                else :
                    if sellAlgorithm(d['buyData'],d['sellData'],buy_price,orderType) :
                        time.sleep(0.5)
                        isToBuy = True
                        logging.info("Analyzing to Buy...")
                        time.sleep(5)
    except KeyError as e :
        trade(topicId)
    except Exception as e:
        sendEmail("Algorithm has crashed.")
        logging.exception(f"ERROR {e}")
        traceback.print_exc()
        exit()


bitcoinPriceDiff = 10
stoploss = 1.5
bookprofit = 1.5
ignores = [0,8]

thread1 = threading.Thread(target=collectBitcoinPriceFromProbo, args=())
thread2 = threading.Thread(target=trade, args=([2449]))

thread1.start()
thread2.start()