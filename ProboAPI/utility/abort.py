from datetime import datetime,timezone

def abort(title : str,isToBuy : bool ) -> bool :
    minutes = int(title[-9:][:8].split()[0][-2:])
    now = datetime.now()
    current_minute = now.minute
    if current_minute >= minutes:
        minutes = 60 + minutes
    if minutes - current_minute <= 2  and isToBuy:
        return True