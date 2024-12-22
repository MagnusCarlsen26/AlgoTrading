from utility.utils import getCurrTemp, getSource
from utility.api import buy
from datetime import datetime
import logging

logging.basicConfig(
    filename='logs/history_logs.txt', 
    level=logging.INFO,
    filemode='a', 
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def lastMinuteBuyStrat( target_temperature, gradient, eventId : int) :
    
    try :
        prev = False
        source = getSource(eventId)
        while True:
            currTemp = getCurrTemp(source)[:2]

            if not prev :
                prev = currTemp
                print(f"Update CurrTemp = {currTemp}, {datetime.now()}")
                logging.info(f"Update CurrTemp = {currTemp}, {datetime.now()}")
            elif prev != currTemp:
                prev = currTemp
                print(f"Update CurrTemp = {currTemp}, {datetime.now()}")
                logging.info(f"Update CurrTemp = {currTemp}, {datetime.now()}")

            if gradient > 0 :
                if currTemp>=target_temperature :
                    buy( eventId, 9.5, 'yes',1 )
                    print("Buying yes")
                    logging.info("Buying yes")
                    break
            else :
                if currTemp<target_temperature :
                    buy( eventId, 9.5, 'no',1 )
                    print("Buying no")
                    logging.info("Buying no")
                    break
    except Exception as e:
        logging.error(f"Error in lastMinuteBuyStrat {e}")