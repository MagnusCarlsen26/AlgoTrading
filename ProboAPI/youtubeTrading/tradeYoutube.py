# import requests
from dotenv import load_dotenv
import os
from utility.api import collectEventPrice, getEventIds, buyBook, buy
import threading
import time
from typing import Literal
import logging
from datetime import datetime
from utils import ytAPI
from strategies import interpolateStrat, lastMinuteBuyStrat
from strategies import calcTimeStepsLeft
import json

configs = {
    "CTRL - Official Trailer": {
        "video_id": "KEfeMPGj-Dw",
    
    },
    "Linkin Park - Heavy Is The Crown": {
        "video_id": "5FrhtahQiRc",
    },
    "MrBeast - 100 Identical Twins" : {
        "video_id": "snX5YyflrGw"
    },

}

def getViews(video_id,target_count,view_rate,title, endTime,history_view_rate) :
    
    average_history_view_rate = 0
    for i in range(-1,-4,-1):
        average_history_view_rate += int(list(history_view_rate[i].values())[0])
    average_history_view_rate = average_history_view_rate//3


    while True:
        view_count = ytAPI(video_id)
        with open(f"logs/views.txt","w") as f:
            f.write(f"{title}\n")
            f.write(f"curr views = {int(view_count):,}\n")
            f.write(f"target views = {int(target_count):,}\n")
            f.write(f"difference = {int(target_count - float(view_count)):,}\n")
            f.write(f"Time stamp left = {calcTimeStepsLeft(endTime)}\n")
            f.write(f"Average Required = {int(target_count - float(view_count))//calcTimeStepsLeft(endTime)}\n")
            f.write(f"view rate = {int(average_history_view_rate):,}\n")
            f.write(f"Prev view rate = {(history_view_rate[-1])}\n")
            f.write(f"Prev view rate = {(history_view_rate[-2])}\n")
            f.write(f"Prev view rate = {(history_view_rate[-3])}\n")
        time.sleep(0.1)


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
    # target_time = datetime.strptime(util[6] + " " + util[7][:-1], "%I:%M %p").time()
    
    # with open('config.json', 'r',encoding="utf-8") as file:
    #     videosData = json.load(file)
    # history_view_rate = videosData[yt_title]["history_view_rate"]


    
    # getViews( configs[yt_title]["video_id"], target_views, view_rate=13000, title=eventInfo['title'], endTime = target_time, history_view_rate= history_view_rate )
    # interpolateStrat(target_views, target_time,yt_title)
    # buyAlgorithm( yt_title, target_time, target_views )
    lastMinuteBuyStrat(eventId,target_views, configs[yt_title]["video_id"],yt_title)

fetchQuestion(int(input("Enter Event id : ")))