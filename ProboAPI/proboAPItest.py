import requests
from dotenv import load_dotenv
import os
from save import save
from time import gmtime, strftime
import random
import time
import websocket
import json
import threading
import queue

load_dotenv()

authorization = os.environ.get('Authorization_Dummy') 
url = 'https://prod.api.probo.in/api/'
bitcoinEventId = [2449]

def fetch( endpoint: str , headers: dict , data: dict , method  ) :
    new_url = url + endpoint
    
    try:
        if method == 'POST' : 
            response = requests.post( new_url , headers = headers , json = data )
        elif method == 'GET': 
            response = requests.get( new_url , headers = headers , params = data )
        elif method == 'PUT' :
            response = requests.put( new_url , headers = headers , json = data )

        if response.status_code == 200 :
            response = response.json()
            if response['isError'] :
                print('ERROR : ' , response['message'])
            else : 
                return response['data']
        else :
            print(f'Error : {response.status_code}')
            print(response.text)
    except NameError as e:
        print('Error Occured')
        fetch(endpoint , headers , data, method )

def buy( eventId : int , buy_price : float , yesno : str , quantity : int = 1) -> int :
    endpoint = 'v1/oms/order/initiate'
    headers = {
        "accept": "*/*",
        "appid": "in.probo.pro",
        "authorization": authorization,
        "content-type": "application/json",
        "origin": "https://trading.probo.in",
        "priority": "u=1, i",
        "referer": "https://trading.probo.in/",
        "x-device-os": "ANDROID",
        "x-version-name": "10"
    }

    data = {
        "event_id" : eventId,
        "offer_type" : 'buy' if yesno == 'yes' else 'sell',
        "order_type"  : "LO",
        "l1_order_quantity" : quantity,
        "l1_expected_price" : str(buy_price)
    }

    data = fetch( endpoint , headers , data , 'POST')
    order_id = data['id']
    return order_id

def buyBook( eventId : int ) -> dict :
    endpoint = 'v3/tms/trade/bestAvailablePrice'
    headers = {
        "accept": "*/*",
        "accept-language": "en",
        "appid": "in.probo.pro",
        "authorization": authorization,
        "content-type": "application/json",
        "if-none-match": 'W/"217c-77YJofEzYutmC1wBp1K0t2omdrk"',
        "origin": "https://trading.probo.in",
        "priority": "u=1, i",
        "referer": "https://trading.probo.in/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-device-os": "ANDROID",
        "x-version-name": "10",
    }
    data = {
        'eventId' : eventId
    }
    data = fetch( endpoint , headers , data , 'GET')

    try:
        ltp = data['ltp']
        buyData = data['available_qty']['buy']
        sellData = data['available_qty']['sell']
        title = data['event_details']['event_name']

        return { 'ltp' : ltp , 'buyData' : buyData  , 'sellData' : sellData , 'title' : title}
    except TypeError as e :
        print(e)
        print(data)

def cancel_order(event_id, order_id, ):
    endpoint = f"v1/oms/order/cancel/{order_id}?eventId={event_id}"
    headers = {
        "accept": "*/*",
        "accept-language": "en",
        "appid": "in.probo.pro",
        "authorization": authorization, # Parameterized auth token
        "content-type": "application/json",
        "origin": "https://trading.probo.in",
        "priority": "u=1, i",
        "referer": "https://trading.probo.in/",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-device-os": "ANDROID",
        "x-version-name": "10",
    }
    data = {
        "investment_visible": 0.5,
        "quantity_visible": 1,
        "request_type": "cancel",
        "quantity_to_cancel": 1
    }

    response = fetch(endpoint, headers, data, 'PUT')

def sell( sell_price : float, order_id : int ) :
    endpoint = 'v2/oms/order/exit'
    headers = {
        "accept": "*/*",
        "accept-language": "en",
        "appid": "in.probo.pro",
        "authorization": authorization,
        "content-type": "application/json",
        "origin": "https://trading.probo.in",
        "priority": "u=1, i",
        "referer": "https://trading.probo.in/",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-device-os": "ANDROID",
        "x-version-name": "10",
    }
    data = {
    "exit_params": [
            {
                "exit_price": sell_price, 
                "order_id": order_id
            }
        ]
    }
    fetch( endpoint , headers , data , 'PUT' )

def trade_status(eventId : int , order_id: int):

    endpoint = 'v2/tms/trade/userTradesPerEvent'
    headers = {
        "accept": "*/*",
        "accept-language": "en",
        "appid": "in.probo.pro",
        "authorization": authorization,
        "content-type": "application/json",
        "if-none-match": "W/\"16cf-LwV2VgqKZSt/oiMASyJg+AssC8c\"",
        "origin": "https://trading.probo.in",
        "priority": "u=1, i",
        "referer": "https://trading.probo.in/",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-device-os": "ANDROID",
        "x-version-name": "10",
    }
    data = {
        'eventId' : eventId
    }
    data = fetch(endpoint , headers , data , 'GET')

    trades = data['records']['tradeSummary']

    for trade in trades :
        for tr in trade['sectionData'] :
            if tr['order_id'] == order_id :
                status = trade['sectionTitle']
                if status == 'Pending Orders' :
                    return 'Pending'
                elif status == 'Matched Orders' :
                    return 'Matched'
                elif status == 'Exited Orders' :
                    return f'Exited {tr['profit']}'
                elif status == 'Cancelled Orders':
                    return 'Cancelled'   
                elif status == 'Exiting Orders':
                    return 'Exiting'

    available_qty = data['records']['availableQty']
    print(available_qty)

def getEventIds( topicIds : list[int] ) :
    endpoint = 'v1/product/arena/events/v2'
    headers = {
        "accept": "*/*",
        "accept-language": "en",
        "appid": "in.probo.pro",
        "authorization": authorization,
        "content-type": "application/json",
        "origin": "https://trading.probo.in",
        "priority": "u=1, i",
        "referer": "https://trading.probo.in/",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-device-os": "ANDROID",
        "x-version-name": "10",
    }
    data = {
        "page": 1,
        "categoryIds": [],
        "topicIds": topicIds,
        "eventIds": [],
        "followedOnly": False,
        "filter": {}
    }
    data = fetch( endpoint , headers , data , 'POST')['records']['events']
    return [ d['id'] for d in data ]

def collectData( topicId : int , q ) :
    while True:
        eventId = getEventIds(topicId)[0]
        while True :
            d = buyBook(eventId)
            print('GEFG',d)
            if d['buyData'] == {} :
                break
            save('yes' , d['buyData'] , d['title'][-9:][:8].replace(':','-') ,  strftime("%Y-%m-%d %H:%M:%S", gmtime()) , q.get() )
            save('no' , d['sellData'] , d['title'][-9:][:8].replace(':','-') ,  strftime("%Y-%m-%d %H:%M:%S", gmtime()) , q.get() )

def buyAlgorithm( buyBook : dict ) :
    x = random.random()
    if x < 0.8 :
        return 0
    else:
        return 9.6

def sellAlgorithm( buyBook : dict ) :
    x = random.random()
    if x < 0.5 :
        return 0
    else:
        return 1

def trade( topicId : list[int] , stoploss : float) : 
    while True:
        eventId = getEventIds(topicId)[0]
        isToBuy = True
        print(f"eventId = {eventId}")
        while True :
            d = buyBook(eventId)
            if d['buyData'] == {}:
                break
            if isToBuy :
                print("Analyzing to Buy...")
                buy_price = buyAlgorithm(d['buyData'])
                if  buy_price:
                    print(f"Buying at {buy_price}.")
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
                        sell( min(buy_price + stoploss,9.5) , order_id)
                        isToBuy = 0
                    else:
                        print(f"STATUS = {status}.............")
            else :
                print("Analyzing for selling...")
                if sellAlgorithm(buyBook) :
                    cancel_order(eventId,order_id)
                    sell(0.5 , order_id)
                    time.sleep(0.5)
                    profit = (trade_status(eventId,order_id).split()[-1])
                    print(f"Order sold, profit = {profit}")
                    isToBuy = 1
            time.sleep(5)

def getBitcoinPrice(q) :

    def on_message(ws,message):
        data = json.loads(message)

        if data.get("t") == "d" and data.get("d", {}).get("b", {}).get("p") == "crypto/btcusdt":
            currBitcoinPrice = data["d"]["b"]["d"]["closePrice"]
            q.put(currBitcoinPrice)

    def on_error(ws,error) :
        print(f"Error: {error}")

    def on_close(ws,close_status_code, close_msg):
        print(f"Closed with status {close_status_code}: {close_msg}")

    def on_open(ws):
        subscription_request = {
            "t": "d",
            "d": {
                "r": 2,  
                "a": "q", 
                "b": {
                    "p": "crypto/btcusdt",  
                    "h": ""  
                }
            }
        }
        ws.send(json.dumps(subscription_request))

    ws_app = websocket.WebSocketApp(
        "wss://s-apse1a-nss-6013.asia-southeast1.firebasedatabase.app/.ws?v=5&p=1:530071772200:web:38ba8735b6fd3ff69a291d&ns=prod-probo-realtime-db-2",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws_app.on_open = on_open
    ws_app.run_forever(ping_interval=30, ping_timeout=10)  

q = queue.Queue()
bitcoinThread = threading.Thread(target=getBitcoinPrice , args =(q,))
collectDataThread = threading.Thread(target=collectData , args=(bitcoinEventId,q,))

collectDataThread.start()
bitcoinThread.start()
