import os
import requests
import json
import time

# Load crypto data from json file
with open('data/crypto_meta_data.json', 'r') as f:
    crypto_data = json.load(f)

start_time_str = "January 1, 2009"
end_time_str = "February 24, 2023"


year_in_seconds = 31536000  # 1 year in seconds
time_period = year_in_seconds

for crypto in crypto_data:
    crypto_id = crypto['crypto_id']
    file_name = crypto['file_name']
    print(f'start downloading {file_name.upper()} historical data')

    folder_path = f"data/{file_name}"
    os.makedirs(folder_path, exist_ok=True)

    start_time = int(time.mktime(time.strptime(start_time_str, "%B %d, %Y")))
    end_time = int(time.mktime(time.strptime(end_time_str, "%B %d, %Y")))

    while end_time > start_time:
        api_url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={crypto_id}&convertId=2781&timeStart={start_time}&timeEnd={start_time + time_period}"

        response = requests.get(api_url)

        if response.status_code == 200:
            json_data = json.loads(response.text)

            # load existing data from file or create a new file
            file_path = f"{folder_path}/{file_name}_historical_data.json"
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
            else:
                data = []

            # check if the latest timestamp in the file is before the start_time of the current request
            latest_timestamp = int(
                time.mktime(time.strptime(data[-1]['timeClose'], "%Y-%m-%dT%H:%M:%S.%fZ"))) if data else 0
            if latest_timestamp < start_time:
                # append new data to existing data and write it back to the file
                data.extend(json_data['data']['quotes'])
                with open(file_path, 'w') as f:
                    json.dump(data, f)
                    print(f"NEW data saved to {file_path} for the year {time.strftime('%Y', time.localtime(start_time))}")
            else:
                print(f"NO NEW data found for the year {time.strftime('%Y', time.localtime(start_time))}")
        else:
            print("Error fetching data from CoinMarketCap API.")

        start_time = start_time + time_period
        time.sleep(2)  # wait for 5 seconds before making the next request

