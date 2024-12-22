from utility.utils import getCurrTemp, getSource
from utility.api import buy
from datetime import datetime

def lastMinuteBuyStrat( target_temperature, gradient, eventId) :
    
    prev = False
    while True:
        currTemp = getCurrTemp(getSource(eventId))

        if not prev :
            prev = currTemp
            print(f"Update CurrTemp = {currTemp} {datetime.now()}")
        elif prev != currTemp:
            prev = currTemp
            print(f"Update CurrTemp = {currTemp} {datetime.now()}")

        if gradient > 0 :
            if currTemp>=target_temperature :
                buy( eventId, 9.5, 'yes',5 )
                print("Buying yes")
                break
        else :
            if currTemp<target_temperature :
                buy( eventId, 9.5, 'no',5 )
                print("Buying no")
                break