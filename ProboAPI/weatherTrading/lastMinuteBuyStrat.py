from utility.utils import getCurrTemp, getSource
from utility.api import buy
from datetime import datetime

def lastMinuteBuyStrat( target_temperature, gradient, eventId : int) :
    
    prev = False
    source = getSource(eventId)
    while True:
        currTemp = getCurrTemp(source)[:2]

        if not prev :
            prev = currTemp
            print(f"Update CurrTemp = {currTemp}, {datetime.now()}")
        elif prev != currTemp:
            prev = currTemp
            print(f"Update CurrTemp = {currTemp}, {datetime.now()}")

        if gradient > 0 :
            if currTemp>=target_temperature :
                print(eventId)
                buy( eventId, 9.5, 'yes',1 )
                print("Buying yes")
                break
        else :
            if currTemp<target_temperature :
                buy( eventId, 9.5, 'no',1 )
                print("Buying no")
                break