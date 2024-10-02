from utility.utils import ytAPI
from datetime import datetime
import json
import time

def cronUpdateViews():

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

while True:
    cronUpdateViews()
    time.sleep(5*60)