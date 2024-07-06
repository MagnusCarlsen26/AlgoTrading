import requests
from dotenv import load_dotenv
import os
from utility.save import save
import json
from datetime import datetime,timezone
import websocket
from typing import Literal
import logging
import traceback
from requests.exceptions import ConnectionError, Timeout, RequestException
from urllib3.exceptions import MaxRetryError, NewConnectionError
import time

load_dotenv()

authorization_dummy = os.environ.get('Authorization_Dummy') 
authorization_real = os.environ.get('Authorization_Real')
url = 'https://prod.api.probo.in/api/'
prices = [str(i/2) for i in range(1,20)]
with open('config.json','r') as f:
    config = json.load(f)

# logging.basicConfig(filename='apiErrorlogs.txt', level=logging.INFO,filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def fetch( endpoint: str , headers: dict , data: dict , method = Literal['POST','GET','PUT']  ) :
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
                # EXIT THE PROGRAM
            else : 
                return response['data']
        else :
            print(f'Error : {response.status_code}')
            print(response.text)
            # EXIT THE PROGRAM
    except (ConnectionError, Timeout, MaxRetryError, NewConnectionError) as e:
        return fetch(endpoint,headers,data,method)
    else:
        print(f"Exception while fetching() ")
        traceback.print_exc()
        # Exit the program
def buy( eventId : int , buy_price : float , yesno : Literal['yes','no'] , quantity : int = 1) -> int :
    try:
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
        # this if isn't needed but still
        if 'id' not in data :
            return buy(eventId,buy_price,yesno,quantity)
        order_id = data['id']
        return order_id
    except Exception as e:
        traceback.print_exc()
        logging.exception(f"{e}Error in buy()")
        logging.exception(e)

def buyBook( eventId : int ) -> dict :
    endpoint = 'v3/tms/trade/bestAvailablePrice'
    headers = config["buyBook"]
    headers["authorization"] = authorization_dummy
    data = {
        'eventId' : eventId
    }

    try:
        data = fetch( endpoint , headers , data , 'GET')
        ltp = data['ltp']
        buyData = data['available_qty']['buy']
        sellData = data['available_qty']['sell']
        title = data['event_details']['event_name']

        return { 'ltp' : ltp , 'buyData' : buyData  , 'sellData' : sellData , 'title' : title}
    except Exception as e :
        traceback.print_exc()
        logging.exception(f"{e}Error in butbook()")
        logging.exception(e)

        
# Confirmation checking IS LEFT
def cancel_order(event_id : int, order_id : int ):
    try:
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
    except Exception as e:
        print(f"{e} in cancel_order()")
        traceback.print_exc()
        logging.exception(f"{e}Error in cancel_order()")
        logging.exception(e)

# Confirmation checking IS LEFT
def sell( sell_price : float, order_id : int ) :
    try:
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
    except Exception as e:
        traceback.print_exc()
        logging.exception(f"{e}Error in sell()")
        logging.exception(e)

def trade_status(eventId : int , order_id: int):
    try:
        endpoint = 'v2/tms/trade/userTradesPerEvent'
        headers = config["trade_status"]
        headers["authorization"] = authorization_real
        data = {
            'eventId' : eventId
        }
        data = fetch(endpoint , headers , data , 'GET')
        if 'records' not in data :
            return trade_status(eventId,order_id)
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
    except Exception as e:
        traceback.print_exc()
        logging.exception(f"{e}Error in trade_status()")
        logging.exception(e)

def getEventIds( topicIds : list[int] ) :
    try:
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

        data = fetch( endpoint , headers , data , 'POST')
        if 'records' not in data :
            return getEventIds(topicIds)
        data = data['records']['events']
        return [ d['id'] for d in data ]
    except Exception as e:
        traceback.print_exc()
        logging.exception(f"{e}Error in getEventIds()")
        logging.exception(e)

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
                currBitcoinPrice = float(data["d"]["b"]["d"]["closePrice"])
                # with open("output.txt", "r") as f:
                #     content = f.read()
                with open("output.txt","w") as f :
                    f.write(str(currBitcoinPrice))
                    # if contenPt == "":
                    #     f.write(f"{currBitcoinPrice},0")
                    # else:
                    #     prevBitcoinPrice = float(content.strip().split(',')[0])  
                    #     f.write(f"{currBitcoinPrice},{round(currBitcoinPrice - prevBitcoinPrice, 2) }")

            except Exception as e:
                print(f"collectBitcoinPrice  : {e}")

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
    
    while True:
        try :
            with open("output.txt" , "w") as file:
                file.write("")
            ws_app = websocket.WebSocketApp(
                "wss://s-apse1a-nss-6013.asia-southeast1.firebasedatabase.app/.ws?v=5&p=1:530071772200:web:38ba8735b6fd3ff69a291d&ns=prod-probo-realtime-db-2",
                on_message=on_message,
            )

            ws_app.on_open = on_open
            ws_app.run_forever(ping_interval=30, ping_timeout=10)  
        except Exception as e:
            logging.exception('Error getting bitcoin price retrying ...',e)
        time.sleep(3)

def collectData( topicId : list[int] ) :
    time.sleep(3)
    try :
        while True:
            eventId = getEventIds([topicId])[2]
            while True :
                d = buyBook(eventId)
                # print(d['buyData'])
                # print(d['title'])
                if d['buyData'] == {} :
                    break
                save('yes' , d['buyData'] , d['title'] , datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] , 'Cricket' )
                save('no' , d['sellData'] , d['title'] , datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] , 'Cricket' )
    except Exception as e:
        print("Error while collecting data ... ",e)
        collectData(topicId)
