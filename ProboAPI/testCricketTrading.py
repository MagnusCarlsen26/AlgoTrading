import time
import threading
from typing import Literal
from utility.api import buyBook,getBuyPrice,collectBitcoinPrice,getEventIds
from utility.abort import abort
from utility.smartQuestionSelector import smartQuestionSelector
from utility.readBitcoinPrice import readBitcoinPrice
import logging
import traceback
from utility.sendEmail import sendEmail
import random
logging.basicConfig(
    filename='trade_log.txt', 
    level=logging.INFO,
    filemode='w', 
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def buyAlgorithm( buyBook : dict , sellBook  : dict ) -> int :
    return random.randint(0,1)

def sellAlgorithm( buyBook : dict , sellBook : dict ,buyPrice : int ,orderType : Literal['yes','no']) -> bool :
    return random.randint(0,1)

def trade( topicId : list[int] ) : 

    try:
         while True:
            eventId = getEventIds([topicId])[0]
            isToBuy = True
            d = buyBook(eventId)
            logging.info(f"Question : {d['title']}")
            while True :
                d = buyBook(eventId)

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


stoploss = 1.5
bookprofit = 1.5

trade(23586)