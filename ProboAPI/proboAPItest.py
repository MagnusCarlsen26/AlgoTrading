import requests
from dotenv import load_dotenv
import os
from save import save
from time import gmtime, strftime

load_dotenv()

authorization = os.environ.get('Authorization_Real') 
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
    except :
        print('Error Occured')
        return fetch( endpoint , headers , data , method )

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
    print(f'order ID : {order_id}')
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
    print(response)

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
                else:
                    print(status)
                return

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

def collectData( topicId : int ) :
    while True:
        eventId = getEventIds(topicId)[0]
        while True :
            d = buyBook(eventId)
            if d['buyData'] == {} :
                break
            save('yes' , d['buyData'] , d['title'][-9:][:8].replace(':','-') ,  strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
            save('no' , d['sellData'] , d['title'][-9:][:8].replace(':','-') ,  strftime("%Y-%m-%d %H:%M:%S", gmtime()) )

def buyAlgorithm( buyBook : dict ) :
    pass

def sellAlgorithm( buyBook : dict ) :
    pass

def trade( topicId : int , stoploss : float) : 
    while True:
        eventId = getEventIds(topicId)[0]
        isToBuy = True
        while True :
            d = buyBook(eventId)
            if d['buyData'] == {}:
                break
            if isToBuy :
                if buyAlgorithm(d['buyData']) :
                    buy_price = buyAlgorithm(d['buyData'])
                    order_id = buy( eventId = eventId , buy_price = buy_price ,  yesno = 'yes' )
                    status = trade_status(eventId=eventId , order_id=order_id)
                    if status == 'Pending' :
                        while status != 'Matched':
                            cancel_order(eventId,order_id)
                            status = trade_status(eventId,order_id)
                        sell( buy_price + stoploss , order_id)
                    isToBuy = 0
            else :
                if sellAlgorithm(buyBook) :
                    sell(0.5 , order_id)
                    profit = int(trade_status(eventId,order_id).split()[-1])
                    isToBuy = 1