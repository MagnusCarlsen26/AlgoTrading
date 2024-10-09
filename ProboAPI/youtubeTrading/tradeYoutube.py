# import requests
from dotenv import load_dotenv
import os
from utility.api import collectEventPrice, getEventIds, buyBook, buy
import threading
import time
from typing import Literal
import logging
from datetime import datetime
from utility.utils import ytAPI,latestQuestionSelector,calcTimeStepsLeft
from strategies import interpolateStrat, lastMinuteBuyStrat
from strategies import calcTimeStepsLeft
import json
import logging

logging.basicConfig(
    filename='logs/history_logs.txt', 
    level=logging.INFO,
    filemode='a', 
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
configs = {
    "Vicky Vidya Ka Woh Wala - Mushkil Hai": {
        "video_id": "Ez6jGMpdCNY",
    },
    "MrBeast - 100 Identical Twins" : {
        "video_id": "snX5YyflrGw"
    },

}

def getViews(eventId) :
    eventInfo = buyBook( eventId )   
    lastIndex = eventInfo['title'].rindex('\'') 
    util = eventInfo['title'][ lastIndex+ 1 :  ].split()
    title = eventInfo['title'][ eventInfo['title'].index('\'') + 1 : lastIndex ]
    video_id = configs[title]["video_id"]
    target_count = float(util[3][:-1])*1000000
    endTime = datetime.strptime(util[6] + " " + util[7][:-1], "%I:%M %p").time()

    # average_history_view_rate = 0
    # for i in range(-1,-4,-1):
        # average_history_view_rate += int(list(history_view_rate[i].values())[0])
    # average_history_view_rate = average_history_view_rate//3


    while True:
        view_count = ytAPI(video_id)
        with open(f"logs/views.txt","w") as f:
            f.write(f"{title}\n")
            f.write(f"curr views = {int(view_count):,}\n")
            f.write(f"target views = {int(target_count):,}\n")
            f.write(f"difference = {int(target_count - float(view_count)):,}\n")
            f.write(f"Time stamp left = {calcTimeStepsLeft(endTime,5)}\n")
            f.write(f"Average Required = {int(target_count - float(view_count))//calcTimeStepsLeft(endTime,5)}\n")
            # f.write(f"view rate = {int(average_history_view_rate):,}\n")
            # f.write(f"Prev view rate = {(history_view_rate[-1])}\n")
            # f.write(f"Prev view rate = {(history_view_rate[-2])}\n")
            # f.write(f"Prev view rate = {(history_view_rate[-3])}\n")
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
    target_time = datetime.strptime(util[6] + " " + util[7][:-1], "%I:%M %p").time()
    logging.info(eventInfo['title'])
    print(eventInfo['title'])
    time_left = calcTimeStepsLeft(target_time,delta=1)
    print(f"Time for event = {time_left} minutes")
    logging.info(f"Time for event = {time_left} minutes")
    if time_left > 2 :
        print(f"Sleeping for 15 secs.")
        logging.info(f"Sleeping for 15 secs.")
        time.sleep((0.25)*60)
        return
    lastMinuteBuyStrat(eventId,target_views, configs[yt_title]["video_id"],yt_title,target_time)

def trade( topicId : list[int] ):
    try :
        while True : 
            eventId = latestQuestionSelector(topicId)
            fetchQuestion(eventId)
    except Exception as e  :
        print("Error in trade()")
        logging.info("Error in trade()")
        print(e)
        logging.info(e)

eventId = int(input("Enter Event Id : "))
while True :
    # fetchQuestion(eventId)
    getViews(eventId)
# trade(452)