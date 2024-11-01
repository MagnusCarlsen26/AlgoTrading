import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time
import math
from datetime import datetime, timedelta
from .api import getEventIds,buyBook
import logging

logging.basicConfig(
    filename='logs/history_logs.txt', 
    level=logging.INFO,
    filemode='a', 
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
load_dotenv()
last_key_worked = 1

def ytAPI(video_id):
    global last_key_worked
    try:
        api_key = os.environ.get(f"YT_API_{last_key_worked}")
        url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                view_count = data['items'][0]['statistics']['viewCount']
                return int(view_count)
            else:
                print('No video found with the given ID.')
                logging.info('No video found with the given ID.')
        else:
            print(f'Error: {response.status_code}')

    except Exception as e:
        logging.error(f"Initial API call failed: {e}")

    for i in range(1, 13):
        try:
            api_key = os.environ.get(f"YT_API_{i}")
            url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}'
            print(f"Trying with API key: YT_API_{i}")
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if 'items' in data and len(data['items']) > 0:
                    view_count = data['items'][0]['statistics']['viewCount']
                    last_key_worked = i 
                    return int(view_count)
                else:
                    print('No video found with the given ID.')
                    logging.info('No video found with the given ID.')
            else:
                print(f'Error with API key YT_API_{i}: {response.status_code}')
                logging.info(f'Error with API key YT_API_{i}: {response.status_code}')

        except Exception as e:
            logging.error(f"API key YT_API_{i} failed: {e}")
            print(f"YT_API_{i} didn't work")
            logging.info(f"YT_API_{i} didn't work")

    print("None of the keys worked, aborting trading.")
    logging.info("None of the keys worked, aborting trading.")
    exit()

def calcTimeStepsLeft( endTime, delta ):   

    curr_time = datetime.now()
    endTime = datetime.combine(curr_time.date(), endTime)
    return math.ceil( (endTime - curr_time)/timedelta(minutes=delta) )

def latestQuestionSelector( topicId : list[int] ) -> int:
    eventIds = getEventIds([topicId])
    if len(eventIds) == 1:
        return eventIds[0]

    latest_time = None
    latest_event = None
    for eventId in eventIds :
        title = buyBook(eventId)['title'][-9:][:8]
        title = datetime.strptime(title,"%I:%M %p")
        if latest_time == None :
            latest_time = title
            latest_event = eventId
        else :
            if latest_time > title :
                latest_time = title
                latest_event = eventId

    return latest_event    