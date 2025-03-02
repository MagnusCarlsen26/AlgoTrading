import os
import requests
import time
from dotenv import load_dotenv

def main():
    load_dotenv()

    start_time = time.time()

    session = requests.Session()

    headers = {
        "accept": "*/*",
        "accept-language": "en",
        "appid": "in.probo.pro",
        "authorization": f"Bearer {os.getenv('PROBO_BEARER_TOKEN')}",
        "content-type": "application/json"
    }


    response = session.get("https://prod.api.probo.in/api/v3/tms/trade/bestAvailablePrice?eventId=3752921", headers=headers)
    
    response.raise_for_status()
    
    data = response.json()
    
    duration = time.time() - start_time
    print(f"Request took: {duration:.2f} seconds")
    
    # print(data)

if __name__ == "__main__":
    main()