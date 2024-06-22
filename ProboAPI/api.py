import requests
from dotenv import load_dotenv
import os
from save import save
from time import gmtime, strftime
import random
import time
import json
from datetime import datetime,timezone
import websocket
import threading
import subprocess

load_dotenv()

authorization_dummy = os.environ.get('Authorization_Dummy') 
authorization_real = os.environ.get('Authorization_Real')
url = 'https://prod.api.probo.in/api/'
prices = [str(i/2) for i in range(1,20)]
with open('config.json','r') as f:
    config = json.load(f)

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
    headers = config["buy"]
    headers["authorization"] = authorization_real
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
    headers = config["buyBook"]
    headers["authorization"] = authorization_dummy
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

def cancel_order(event_id : int, order_id : int ):
    endpoint = f"v1/oms/order/cancel/{order_id}?eventId={event_id}"
    headers = config["cancel_order"]
    headers["authorization"] = authorization_real
    data = {
        "investment_visible": 0.5,
        "quantity_visible": 1,
        "request_type": "cancel",
        "quantity_to_cancel": 1
    }

    response = fetch(endpoint, headers, data, 'PUT')

def sell( sell_price : float, order_id : int ) :
    endpoint = 'v2/oms/order/exit'
    headers = config["sell"]
    headers["authorization"] = authorization_real
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
    headers = config["trade_status"]
    headers["authorization"] = authorization_real
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

def getEventIds( topicIds : list[int] ) :
    endpoint = 'v1/product/arena/events/v2'
    headers = config["getEventIds"]
    headers["authorization"] = authorization_dummy
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

def getBuyPrice( buyBook : dict ) -> int :
    for i in prices:
        if buyBook[i] != 0:
            return float(i)
    return 10

def collectBitcoinPrice() :

    def on_message(ws,message):
        data = json.loads(message)

        if data.get("t") == "d" and data.get("d", {}).get("b", {}).get("p") == "crypto/btcusdt":
            try:
                currBitcoinPrice = data["d"]["b"]["d"]["closePrice"]
                with open("output.txt" , "w") as file:
                    file.write(currBitcoinPrice)
            except Exception as e:
                print(f"collectBitcoinPrice : on_message : {e}")

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

    try :

        ws_app = websocket.WebSocketApp(
            "wss://s-apse1a-nss-6013.asia-southeast1.firebasedatabase.app/.ws?v=5&p=1:530071772200:web:38ba8735b6fd3ff69a291d&ns=prod-probo-realtime-db-2",
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )

        ws_app.on_open = on_open
        ws_app.run_forever(ping_interval=30, ping_timeout=10)  
    except Exception as e:
        print('Error getting bitcoin price retrying ...',e)
        collectBitcoinPrice()

def collectData( topicId : list[int] ) :
    try :
        while True:
            eventId = getEventIds([topicId])[0]
            while True :
                d = buyBook(eventId)
                if d['buyData'] == {} :
                    break

                save('yes' , d['buyData'] , d['title'][-9:][:8].replace(':','-') , datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] , 'Bitcoin' )
                save('no' , d['sellData'] , d['title'][-9:][:8].replace(':','-') , datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] , 'Bitcoin' )
    except Exception as e:
        print("Error while collecting data ... ",e)
        collectData(topicId)
