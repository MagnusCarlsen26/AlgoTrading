from bs4 import BeautifulSoup
from utility.api import getSlug
import json
import re
import requests
import logging

logging.basicConfig(
    filename='logs/history_logs.txt', 
    level=logging.INFO,
    filemode='a', 
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

with open('logs/config.json','r') as f:
    config = json.load(f)

def extractVideoIdFromHTML( html : str ) -> str : 
        soup = BeautifulSoup(html.text, "html.parser")

        script_tag = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
        j = json.loads(script_tag.string)
        link = j["props"]["pageProps"]["props"]["eventMeta"]["source_of_truth"]

        return link

def getSource( eventId : int ) -> str:

    try:
        slug = getSlug( [26400] , eventId )
        response = requests.get(f"https://probo.in/events/{slug}")
        response.raise_for_status()  

        return extractVideoIdFromHTML(response)

    except requests.exceptions.RequestException as err:
        print(err)

def getWeatherEventIds() -> list :
    import requests
    url = "https://probo.in/events/weather"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": "_dcmn_p=wDtJY2lkPW94U3pBbWRsRW9ZblVmTnVBb1E; _dcmn_p=wDtJY2lkPW94U3pBbWRsRW9ZblVmTnVBb1E; probo_user_mobile=9328576258; probo_user_session_id=5283fd9b-cb63-4079-b96b-d84f73199e73; probo_user_id=26375270; probo_user_onboarding_type=OB_1; probo_new_user=false; probo_user_token=3nLLGeuOt1O9mPp1zXnON8MLIPdlH1FcvBfEqckJIng%3D; probo_user_preferred_language=en",
        "Referer": "https://www.google.com/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    html = requests.get(url, headers=headers)

    soup = BeautifulSoup(html.text, "html.parser")

    script_tag = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
    j = json.loads(script_tag.string)
    j = j["props"]["pageProps"]["props"]["events"]["records"]["events"][0]

    print(j)

def getCurrTemp(url):

    headers = config["accuWeather"]
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        temp_element = soup.find(class_="temp")
        
        if temp_element:
            return(temp_element.text.strip())
        else:
            print("Class 'temp' not found.")
    else:
        print(f"Error: {response.status_code}")
