from utils import ytAPI
import time
from datetime import datetime, timedelta
import math
from utility.api import buy
import json

quantity = 1

def calcTimeStepsLeft( endTime ):   

    curr_time = datetime.now()
    endTime = datetime.combine(curr_time.date(), endTime)
    return math.ceil( (endTime - curr_time)/timedelta(minutes=5) )

def lastMinuteBuyStrat(eventId,target_views,video_id,title ) :

    """
        Let's say question deadline is 4:45 PM and at 4:41 PM required views = 13K.
        So there is only one time step left. Let's say current view rate is 12K/time_step.
        So at the last time step any thing can happen. 

        This code will start to run at 4:43:30 PM. It will aggresively check for curr views. Once the 
        views are updated, the code will by yes/no at ₹9.5. Theoritically it can buy all the orders
        but I will limit it during testing.
    """
    prev = None
    while True:

        curr_views = ytAPI(video_id)
        if prev == None :
            prev = curr_views
            print(f"prev views = {int(prev):,}")
            continue

        if curr_views != prev :

            if target_views < curr_views :
                buy(eventId,9.5,'yes',5)
                print("Buying yes")
                print(curr_views)
                print(time.time())
                return
            else :
                prev = curr_views
                print(f"Views updated = {prev}")

def interpolateStrat( target_views, endTime, yt_title) :

    timeStampsLeft = calcTimeStepsLeft(endTime)
    currViews = ytAPI()
    history_view_rate = 0

    for count in range(1,4):
        average_view_rate = 0
        for i in range(-1,-count+1,-1):
            average_view_rate += history_view_rate
        average_view_rate = average_view_rate//3

        interpolated_prediction = currViews + average_view_rate*timeStampsLeft
        
        diff = interpolated_prediction - target_views

        ratio = diff/average_view_rate

        print(f"For count = {count}")
        print(f"Diff = {diff} , ratio = {ratio}")