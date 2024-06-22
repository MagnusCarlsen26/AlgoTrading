import time
import threading
from utility.api import buy,buyBook,cancel_order,sell,trade_status,getBuyPrice,collectBitcoinPrice,collectData
from utility.abort import abort
from utility.smartQuestionSelector import smartQuestionSelector
import logging
from pydub import AudioSegment
from pydub.playback import play

prevBitcoinPrice = None
logging.basicConfig(filename='trade_log.txt', level=logging.INFO,filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def buyAlgorithm( buyBook : dict , sellBook  : dict ) -> int :
    global prevBitcoinPrice
    with open("output.txt", "r") as file :
        try:
            currBitcoinPrice = float(file.read().strip())
        except ValueError as e:
            return 0

    if prevBitcoinPrice == None :
        prevBitcoinPrice = currBitcoinPrice
        return 0
    
    diff = currBitcoinPrice - prevBitcoinPrice

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
        logging.info(f"Difference = {diff}")
        return factor*currPrice
    return 0

def sellAlgorithm( buyBook : dict , sellBook : dict ,buyPrice : int ,orderType : str) -> bool :
    global prevBitcoinPrice
    with open("output.txt", "r") as file :
        try:
            currBitcoinPrice = float(file.read().strip())
        except ValueError as e:
            print(f"save : error : {e}")
            return 0
        
    if prevBitcoinPrice == None :
        prevBitcoinPrice = currBitcoinPrice
        return 0
    
    diff = currBitcoinPrice - prevBitcoinPrice
    
    if orderType == 'yes' :
        currPrice = getBuyPrice(buyBook)
        factor = -1
    else:
        currPrice = getBuyPrice(sellBook)
        factor = 1
    
    if factor*diff > bitcoinPriceDiff:
        logging.info(f"Difference = {diff}")
        return True
    if buyPrice - (currPrice - 0.5) >= stoploss :
        return True
    return False    

def trade( topicId : list[int] ) : 
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
        logging.exception(f"ERROR {e}")
        sound = AudioSegment.from_file("alert.mp3", format="mp3")
        play(sound)

        exit()


bitcoinPriceDiff = 8
stoploss = 1.5
bookprofit = 1.5
ignores = [0,8]

thread1 = threading.Thread(target=collectBitcoinPrice, args=())
thread2 = threading.Thread(target=trade, args=([2449]))

thread1.start()
thread2.start()