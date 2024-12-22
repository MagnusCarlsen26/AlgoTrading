import json
from utility.api import getEventIds, buyBook
import re
from lastMinuteBuyStrat import lastMinuteBuyStrat
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

def trade( topicId : list[int] ):
    
    eventId = (getEventIds(topicId)[0])
    event = buyBook(eventId)

    logging.info(event["title"])
    print(event["title"])
    
    target_temperature = (re.search(r'(\d{1,3})°[CF]', event["title"])).group(1)

    lastMinuteBuyStrat(target_temperature, gradient, eventId)

gradient = int(input("Gradient = "))
trade([26400])