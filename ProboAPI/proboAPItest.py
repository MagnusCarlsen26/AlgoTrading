import time
import threading
from typing import Literal
from utility.api import buy,buyBook,cancel_order,sell,trade_status,getBuyPrice,collectBitcoinPrice,collectData
from utility.abort import abort
from utility.smartQuestionSelector import smartQuestionSelector
from utility.readBitcoinPrice import readBitcoinPrice
from utility.sendEmail import sendEmail
import logging
import traceback

logging.basicConfig(
    filename='trade_log.txt', 
    level=logging.INFO,
    filemode='w', 
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

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
        
    if factor*diff >= bitcoinPriceDiff :
        logging.info(f"Difference = {diff}")
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
        logging.info(f"Selling because difference = {diff}.")
        return True
    if buyPrice - (currPrice - 0.5) >= stoploss :
        logging.info(f"Selling because of stoploss.")
        return True
    return False    

def trade( topicId : list[int] ) : 
    while True :
        with open("output.txt") as f:
            x = f.read()
            if x != "":
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
                if abort(d['title'],isToBuy) :
                    break
                if isToBuy:
                    buy_price = buyAlgorithm(d['buyData'],d['sellData'])
                    if buy_price != 0:
                        orderType = 'yes' if buy_price > 0 else 'no'
                        buy_price = abs(buy_price)
                        # SEND EMAIL
                        logging.info(f"Buying {orderType} for {buy_price}...")
                        order_id = buy( eventId , buy_price , orderType )
                        time.sleep(0.2)
                        status = trade_status(eventId, order_id)
                        if status == 'Pending' :
                            logging.info("Order didn't match, cancelling it.")
                            while status != 'Cancelled':
                                cancel_order(eventId,order_id)
                                status = trade_status(eventId,order_id)
                            logging.info("Order Cancelled")
                        elif status == 'Matched':
                            sell( min(buy_price + bookprofit,9.5) , order_id)
                            isToBuy = False
                            logging.info("Analyzing for selling...")
                        else:
                            logging.info(f"STATUS = {status}.............")
                else :
                    if 'Exited' in trade_status(eventId,order_id):
                        profit = (trade_status(eventId,order_id).split()[-1])
                        # SEND EMAIL
                        logging.info(f"Order sold, profit = {profit}")
                        isToBuy = True
                        logging.info("Analyzing to Buy...")
                        continue
                    if sellAlgorithm(d['buyData'],d['sellData'],buy_price,orderType) :
                        cancel_order(eventId,order_id)
                        sell(0.5 , order_id)
                        time.sleep(0.5)
                        profit = (trade_status(eventId,order_id).split()[-1])
                        logging.info(f"Order sold, profit = {profit}")
                        isToBuy = True
                        logging.info("Analyzing to Buy...")
                # time.sleep(5)
    except Exception as e:  
        sendEmail("Algorithm has crashed.")
        logging.exception(f"ERROR {e}")
        traceback.print_exc()
        exit(1)


bitcoinPriceDiff = 8
stoploss = 1.5
bookprofit = 1.5
ignores = [0,8]

thread1 = threading.Thread(target=collectBitcoinPrice, args=())
thread2 = threading.Thread(target=trade, args=([2449]))

thread1.start()
thread2.start()