# import requests
from dotenv import load_dotenv
import os
from utility.api import collectEventPrice, getEventIds, buyBook, buy
import threading
import time
from typing import Literal
import logging
from datetime import datetime
from utility.utils import ytAPI,latestQuestionSelector,calcTimeStepsLeft,getVideoId
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
    "Kabhi Main Kabhi Tum - Ep 33" : {
        "video_id" : "EiNlWJfXKlU"
    },
    "BABYMONSTER - 'CLIK CLAK" : {
        "video_id" : "o0oW3lPoOXM"
    }
}

def getViews(eventId) :
    eventInfo = buyBook( eventId )
    print(eventInfo)   
    lastIndex = eventInfo['title'].rindex('\'') 
    util = eventInfo['title'][ lastIndex+ 1 :  ].split()
    title = eventInfo['title'][ eventInfo['title'].index('\'') + 1 : lastIndex ]
    video_id = configs[title]["video_id"]
    target_count = float(util[3][:-1])*1000000
    endTime = datetime.strptime(util[6] + " " + util[7][:-1], "%I:%M %p").time()

    while True:
        view_count = ytAPI(video_id)
        with open(f"logs/views.txt","w") as f:
            f.write(f"{title}\n")
            f.write(f"curr views = {int(view_count):,}\n")
            f.write(f"target views = {int(target_count):,}\n")
            f.write(f"difference = {int(target_count - float(view_count)):,}\n")
            f.write(f"Time stamp left = {calcTimeStepsLeft(endTime,5)}\n")
            f.write(f"Average Required = {int(target_count - float(view_count))//calcTimeStepsLeft(endTime,5)}\n")
        current_minutes = datetime.now().minute
        sleep_duration = 5 if current_minutes % 5 < 3 else 0
        time.sleep(sleep_duration)


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
    
    lastMinuteBuyStrat(eventId,target_views,target_time)

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

trade(452)