import time
import threading
from typing import Literal
from utility.api import buy,buyBook,cancel_order,sell,trade_status,getBuyPrice,collectBitcoinPriceFromProbo,collectBitcoinData,collectBitcoinPriceFromBinance
from utility.abort import abort
from utility.smartQuestionSelector import smartQuestionSelector
from utility.readBitcoinPrice import readBitcoinPrice
from utility.sendEmail import sendEmail
import logging
import traceback

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
        print(f"Trying to buy {factor}, diff = {diff}")
        logging.info(f"Trying to buy {factor}, diff = {diff}")
        return factor*currPrice
    return 0

def sellAlgorithm( buyBook : dict , sellBook : dict ,buyPrice : int ,orderType : Literal['yes','no']) -> bool :
    global prevBitcoinPrice
    currBitcoinPrice = readBitcoinPrice()
    if prevBitcoinPrice != 0 :
        diff = currBitcoinPrice - prevBitcoinPrice
    else :
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
        print(f"Trying to sell at {currPrice - 0.5} because difference = {diff}.")
        logging.info(f"Trying to sell at {currPrice - 0.5} because difference = {diff}.")
        return True
    if buyPrice - (currPrice - 0.5) >= stoploss :
        print(f"Trying to sell at {currPrice - 0.5} because of stop loss.")
        logging.info(f"Trying to sell at {currPrice - 0.5} because of stop loss.")
        return True
    return False    

def trade( topicId : list[int] ) : 
    while True :
        with open("logs/output.txt") as f:
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
            print(f"Working on {d['title']}")
            while True :
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
                            print("Order didn't match, cancelling it.")
                            while status != 'Cancelled':
                                cancel_order(eventId,order_id)
                                status = trade_status(eventId,order_id)
                            print("Order Cancelled.")
                            logging.info("Order Cancelled")
                        elif status == 'Matched':
                            sell( min(buy_price + bookprofit,9.5) , order_id)
                            isToBuy = False
                            print("Analyzing for selling...")
                            logging.info("Analyzing for selling...")
                        else:
                            print(f"STATUS = {status}.............")
                            logging.info(f"STATUS = {status}.............")
                else :
                    if 'Exited' in trade_status(eventId,order_id):
                        profit = (trade_status(eventId,order_id).split()[-1])
                        # SEND EMAIL
                        print(f"Order sold, profit/loss = {profit}.")
                        logging.info(f"Order sold, profit/loss = {profit}.")
                        print("Analyzing to Buy...")
                        logging.info("Analyzing to Buy...")
                        isToBuy = True
                        continue
                    if sellAlgorithm(d['buyData'],d['sellData'],buy_price,orderType) :
                        cancel_order(eventId,order_id)
                        sell(0.5 , order_id)
                        time.sleep(0.5)
                        profit = (trade_status(eventId,order_id).split()[-1])
                        logging.info(f"Order sold, Loss = {profit}")
                        isToBuy = True
                        print(f"Analyzing to buy.")
                        logging.info("Analyzing to Buy...")
                # time.sleep(5)
    except Exception as e:  
        sendEmail("Algorithm has crashed.")
        logging.exception(f"ERROR {e}")
        traceback.print_exc()
        exit(1)


bitcoinPriceDiff = 5
stoploss = 1.5
bookprofit = 1.5
ignores = [0,1,8]

# thread1 = threading.Thread(target=collectBitcoinPriceFromProbo, args=())
thread2 = threading.Thread(target=collectBitcoinPriceFromBinance, args=())
# thread3 = threading.Thread(target=collectBitcoinData,args=([2449]))
thread4 = threading.Thread(target=trade, args=([2449]))

# thread1.start()
thread2.start()
# thread3.start()
thread4.start()