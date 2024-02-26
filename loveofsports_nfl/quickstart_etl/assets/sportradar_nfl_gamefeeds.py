import json
from datetime import datetime
import os
import requests

from dagster import asset


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

    os.makedirs("zepor-database", exist_ok=True)
    with open(
        f"zepor-database/GameFeed_{current_date}.txt", "w", encoding="utf-8"
    ) as f:
        json.dump(response.text, f, ensure_ascii=False, indent=4)
