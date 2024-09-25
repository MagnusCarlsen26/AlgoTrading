from datetime import datetime,timezone
import time

def abort(title : str,isToBuy : bool ) -> bool :
    minutes = int(title[-9:][:8].split()[0][-2:])
    now = datetime.now()
    current_minute = (now.minute + 30 )%60
    if current_minute >= minutes:
        minutes = 60 + minutes
    if minutes - current_minute <= 5  and isToBuy:
        time.sleep(15*1000)
        return True