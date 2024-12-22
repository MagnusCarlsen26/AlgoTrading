from bs4 import BeautifulSoup
from utility.api import getSlug
import json
import re
import requests

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