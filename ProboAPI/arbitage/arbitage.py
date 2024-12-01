import json
from ..utility.save import save

def readBuyBook() :
    while True :
        with open('response.json', 'r') as file:
            data = json.load(file) 
            print(data["isError"])
            break

readBuyBook()
