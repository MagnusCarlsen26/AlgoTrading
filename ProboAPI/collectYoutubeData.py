from utility.api import buyBook,collectEventPrice,getEventIds
from datetime import datetime
from dotenv import load_dotenv
from youtubeTrading.utility.utils import ytAPI
import json
import time
import threading
import asyncio
load_dotenv()

configs = {
    "Kabhi Main Kabhi Tum - Ep 33" : {
        "video_id" : "EiNlWJfXKlU"
    },
    "BABYMONSTER - 'CLIK CLAK" : {
        "video_id" : "o0oW3lPoOXM"
    },
    "Karol G - Si Antes Te Song" : {
        "video_id" : "QCZZwZQ4qNs"
    },
    "Rose & Bruno Mars - APT Music" : {
        "video_id" : "ekr2nIex040"
    } 
}

def getViewService():

    while True :
        d = {}
        for video in configs :
            video_id = configs[video]["video_id"]
            d[video] = ytAPI(video_id)

        with open('logs/viewService.json', 'w') as json_file:
            json.dump(d, json_file, indent=4)

        current_minutes = datetime.now().minute
        sleep_duration = 5 if current_minutes % 5 < 3 else 0
        time.sleep(sleep_duration)


async def processEvent( eventId ):
    try:
        d = {}
        eventInfo = buyBook(eventId)   
        lastIndex = eventInfo['title'].rindex('\'') 
        util = eventInfo['title'][ lastIndex + 1 :  ].split()
        title = eventInfo['title'][ eventInfo['title'].index('\'') + 1 : lastIndex ]
        with open('logs/viewService.json', 'r') as json_file:
            data = json.load(json_file)
            d["views"] = data[title]

        collectEventPrice(eventId, d)
    except Exception as e:
        print(f"Error processing event {eventId}: {e}")

async def collectYoutubeData(topicId: list[int]):
    try:
        while True:
            eventIds = getEventIds(topicId)
            tasks = [processEvent(eventId) for eventId in eventIds]
            await asyncio.gather(*tasks)

    except Exception as e:
        print(f"Error in collectYoutubeData: {e}")
        await collectYoutubeData(topicId)

def start_collect_youtube_data():
    asyncio.run(collectYoutubeData([452]))

thread1 = threading.Thread(target=getViewService, args=())
thread2 = threading.Thread(target=start_collect_youtube_data)
thread1.start()
thread2.start()