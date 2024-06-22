import time
import threading
from utility.api import buy,buyBook,cancel_order,sell,trade_status,getBuyPrice,collectBitcoinPrice,collectData
from utility.abort import abort
from utility.smartQuestionSelector import smartQuestionSelector

prevdict = {}
currdict = {}

def buyAlgorithm( buyBook : dict , sellBook : dict) -> int :
    global prevdict,currdict

    with open("output.txt", "r") as file :
        try:
            bitcoinPrice = float(file.read().strip())
        except ValueError as e:
            return 0

    buyBook['bitcoinPrice'] = bitcoinPrice
    currdict = buyBook.copy()
    if prevdict == {} :
        prevdict = currdict.copy()
        return
    
    currPrice = getBuyPrice(currdict)
    for ignore in ignores:
        if ignore <= currPrice <= ignore + 2:
            prevdict = currdict.copy()
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
    if prevdict == {} :
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
            eventId = smartQuestionSelector(topicId)
            isToBuy = True
            d = buyBook(eventId)
            print(f"Question : {d['title']}")
            while True :
                d = buyBook(eventId)
                if abort(d['title'],isToBuy) :
                    break
                if isToBuy :
                    buy_price = buyAlgorithm(d['buyData'])
                    if buy_price:
                        print(f"Buying for {buy_price}...")
                        order_id = buy( eventId = eventId , buy_price = buy_price ,  yesno = 'yes' )
                        time.sleep(0.2)
                        status = trade_status(eventId=eventId , order_id=order_id)
                        if status == 'Pending' :
                            print("Order didn't match, cancelling it.")
                            while status != 'Cancelled':
                                cancel_order(eventId,order_id)
                                status = trade_status(eventId,order_id)
                            print("Order Cancelled")
                        elif status == 'Matched':
                            sell( min(buy_price + bookprofit,9.5) , order_id)
                            isToBuy = False
                            print("Analyzing for selling...")
                        else:
                            print(f"STATUS = {status}.............")
                else :
                    if 'Exited' in trade_status(eventId,order_id):
                        profit = (trade_status(eventId,order_id).split()[-1])
                        print(f"Order sold, profit = {profit}")
                        isToBuy = True
                        print("Analyzing to Buy...")
                        continue
                    if sellAlgorithm(d['buyData'],buy_price) :
                        cancel_order(eventId,order_id)
                        sell(0.5 , order_id)
                        time.sleep(0.5)
                        profit = (trade_status(eventId,order_id).split()[-1])
                        print(f"Order sold, profit = {profit}")
                        isToBuy = True
                        print("Analyzing to Buy...")
                # time.sleep(5)
    except Exception as e:
        print("ERROR",e)
        print("Restarting Trade ...")
        trade(topicId)


bitcoinPriceDiff = 10
stoploss = 1.5
bookprofit = 1.5
ignores = [-1,9]

thread1 = threading.Thread(target=collectBitcoinPrice, args=())
thread2 = threading.Thread(target=trade, args=([2449]))

thread1.start()
thread2.start()