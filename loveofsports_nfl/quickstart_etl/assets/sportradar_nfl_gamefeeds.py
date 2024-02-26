import json
from datetime import datetime
import os
import requests

from dagster import asset
from sportradar.simulation.available_recordings import AvailableRecordings


@asset(group_name="NFL", compute_kind="SportRadar API")
def get_available_recordings() -> None:
    url = "https://playback.sportradar.com/graphql"
    rec = AvailableRecordings(url)
    query = rec.construct_query()
    data = rec.post_json_data(query).json()
    current_date = datetime.now().strftime("%Y%m%d")
    os.makedirs("data", exist_ok=True)
    with open(f"data/simulation_{current_date}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@asset(group_name="NFL", compute_kind="MongoDB Zepor")
def get_game_feeds() -> None:
    current_date = datetime.now().strftime("%Y%m%d")
    url = "https://eastus2.azure.data.mongodb-api.com/app/data-dbjkj/endpoint/data/v1/action/findOne"

    payload = json.dumps(
        {
            "collection": "GameFeed",
            "database": "Current_Season",
            "dataSource": "Zepor",
            "projection": {"_id": 1},
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": "7tth2t3D4zPR1MG0mFi337kIpcQijIojPxH1oKMh6aHpvi648Dq2THEUZUwHX2lO",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    # data = get_data_from_mongodb(db_uri=url, database=database, collection=collection)
    os.makedirs("zepor-database", exist_ok=True)
    with open(
        f"zepor-database/GameFeed_{current_date}.txt", "w", encoding="utf-8"
    ) as f:
        json.dump(response.text, f, ensure_ascii=False, indent=4)
