import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time


load_dotenv()

api_key =  os.environ.get('YT_API_2')

def ytAPI(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
                view_count = data['items'][0]['statistics']['viewCount']
                return int(view_count)
        else:
            print('No video found with the given ID.')
    else:
        print(f'Error: {response.status_code}, {response.text}')

def cronUpdateViews():

    while True :
        with open('config.json', 'r',encoding="utf-8") as file:
            videosData = json.load(file)

        for title,data in videosData.items():
            currViews = ytAPI(data["video_id"])

            currTime = datetime.now().strftime("%I:%M %p")

            if len(data["history_views"]) :
                lastViews = int(list(data["history_views"][-1].values())[0])
                data["history_view_rate"].append({ currTime : currViews - lastViews })
            data["history_views"].append({ currTime : currViews })
        
        with open('config.json', 'w') as file:
            json.dump(videosData, file, indent=4)
        
        time.sleep(5*60)

cronUpdateViews()