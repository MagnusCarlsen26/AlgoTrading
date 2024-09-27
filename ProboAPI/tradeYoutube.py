import requests
from dotenv import load_dotenv
import os
from utility.api import collectEventPrice, getEventIds, buyBook, buy
import threading
import time
from typing import Literal
import logging
from datetime import datetime

load_dotenv()

api_key =  os.environ.get('YT_API')

configs = {
    "CTRL - Official Trailer" : {
        "video_id" : 'KEfeMPGj-Dw',
        "history_views" : [17869,22315,22184,18212,16915,21145,15301,18206,26389,],
    },
    # 04:05 PM : 7,461,739
    # 04:10 PM : 7,479,608
    # 04:15 PM : 7,501,923
    # 04:20 PM : 7,524,107
    # 04:25 PM : 7,542,319
    # 04:30 PM : 7,559,234
    # 04:35 PM : 7,580,379
    # 04:40 PM : 7,595,680
    # 04:45 PM : 7,613,886
    # 04:50 PM : 7,640,275
    # 05:00 PM : 7,685,072
    "Linkin Park - Heavy Is The Crown" : { 
        "video_id" : "5FrhtahQiRc",
        "history_views" : [18061,26103,20959,14282,18861,17146,15182,27904,24218]
    }
    # 04:05 PM : 16,059,176
    # 04:10 PM : 16,077,237
    # 04:15 PM : 16,103,340
    # 04:20 PM : 16,124,299
    # 04:25 PM : 16,138,581 
    # 04:30 PM : 16,157,442
    # 04:35 PM :  16,174,588
    # 04:40 PM : 16,189,770
    # 04:45 PM : 16,217,674
    # 04:50 PM : 16,241,892
    # 05:00 PM : 16,291,337 
}

def ytAPI(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
                view_count = data['items'][0]['statistics']['viewCount']
                return view_count
        else:
            print('No video found with the given ID.')
    else:
        print(f'Error: {response.status_code}, {response.text}')

def getViews(video_id,target_count,view_rate,title) :

    while True:
        view_count = ytAPI(video_id)
        with open(f"logs/views.txt","w") as f:
            f.write(f"{title}\n")
            f.write(f"curr views = {int(view_count):,}\n")
            f.write(f"target views = {int(target_count):,}\n")
            f.write(f"difference = {int(target_count - float(view_count)):,}\n")
            # f.write(f"view rate = {int(view_rate):,}\n")
        time.sleep(5)

def saveCurrViews( eventId : int ):
    try :
        while True :
            with open(f"logs/views.txt","r") as f:
                x = (f.read().strip())
                d = { "views" : int(x)}
            
            collectEventPrice( eventId , d)
    except :
        return saveCurrViews( eventId )

def fetchQuestion( eventId : int ):

    eventInfo = buyBook( eventId )    
    lastIndex = eventInfo['title'].rindex('\'') 
    util = eventInfo['title'][ lastIndex+ 1 :  ].split()
    
    yt_title = eventInfo['title'][ eventInfo['title'].index('\'') + 1 : lastIndex ]
    target_views = float(util[3][:-1])*1000000
    target_time = datetime.strptime(util[6] + " " + util[7][:-1], "%I:%M %p" )
    
    getViews( configs[yt_title]["video_id"], target_views, view_rate=13000, title=eventInfo['title'] )
    # buyAlgorithm( yt_title, target_time, target_views )
    # LastMinuteBuy(eventId,target_views, configs[yt_title]["video_id"])

def LastMinuteBuy( eventId,target_views,video_id ) :

    prev = None

    while True:

        curr_views = ytAPI(video_id)
        if prev == None :
            prev = curr_views
            print(f"prev views = {int(prev):,}")
            continue

        if curr_views != prev :
            print(f"Views updated !! {int(curr_views):,}")
            if target_views > curr_views :
                buy( eventId, 9.5, 'no', 1 )
            else :
                buy( eventId, 9.5, 'yes', 1 )
        time.sleep(0.1)

def trade( topicId : list[int] ) : 
    try:
        #  while True:
            eventIds = getEventIds([topicId])
            for eventId in eventIds :
                ## DO THIS ASYNC, this is wrong
                print(eventId)
                threading.Thread(target=fetchQuestion, args=([eventId])).start()
            # isToBuy = True
            # d = buyBook(eventId)
            # logging.info(f"Question : {d['title']}")
            # while True :
            #     d = buyBook(eventId)
            #     if isToBuy:
            #         buy_price = buyAlgorithm(d['buyData'],d['sellData'])
            #         if buy_price != 0:
            #             orderType = 'yes' if buy_price > 0 else 'no'
            #             buy_price = abs(buy_price)
            #             logging.info(f"Buying {orderType} for {buy_price}...")
            #             time.sleep(0.2)
            #             isToBuy = False
            #             logging.info("Analyzing for selling...")
            #     else :
            #         if sellAlgorithm(d['buyData'],d['sellData'],buy_price,orderType) :
            #             time.sleep(0.5)
            #             isToBuy = True
            #             logging.info("Analyzing to Buy...")
            #             time.sleep(5)
    except KeyError as e :
        # trade(topicId)
        print(e)
        pass
    except Exception as e:
        # sendEmail("Algorithm has crashed.")
        # logging.exception(f"ERROR {e}")
        # traceback.print_exc()
        printm(e)
        exit()

                #     break

fetchQuestion(3081106)