from .api import getEventIds
from .api import buyBook
from datetime import datetime

def smartQuestionSelector( topicId : list[int] ) -> int:
    eventIds = getEventIds([topicId])
    if len(eventIds) == 1:
        return eventIds[0]

    title1,title2 = buyBook(eventIds[0])['title'][-9:][:8] , buyBook(eventIds[1])['title'][-9:][:8]

    title1 = datetime.strptime(title1,"%I:%M %p")
    title2 = datetime.strptime(title2,"%I:%M %p")

    if title1 > title2 :
        return eventIds[0]
    else:
        return eventIds[1]
    