import json
from datetime import datetime
import os
import requests


from dagster import asset, MaterializeResult, AssetExecutionContext, MetadataValue

headers = {
    "Content-Type": "application/json",
    "Access-Control-Request-Headers": "*",
    "api-key": "7tth2t3D4zPR1MG0mFi337kIpcQijIojPxH1oKMh6aHpvi648Dq2THEUZUwHX2lO",
}
current_date = datetime.now().strftime("%Y%m%d")
dataSource = "Zepor"
database = "Current_Season"
url = "https://eastus2.azure.data.mongodb-api.com/app/data-dbjkj/endpoint/data/v1/action/find"


@asset(group_name="NFL", compute_kind="MongoDB Zepor")
def get_game_feeds_by_scheduled() -> None:
    payload = json.dumps(
        {
            "collection": "GameFeed",
            "database": database,
            "dataSource": dataSource,
            "projection": {},
            "filter": {
                "scheduled": "2024-01-07T18:00:00+00:00"
            }
        }
    )

    response = requests.request("POST", url, headers=headers, data=payload)
    os.makedirs("zepor-database", exist_ok=True)
    with open(
            f"zepor-database/GameFeed_ids_{current_date}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)


@asset(group_name="NFL", compute_kind="MongoDB Zepor")
def get_game_feeds_by_game_type() -> None:
    payload = json.dumps(
        {
            "collection": "GameFeed",
            "database": database,
            "dataSource": dataSource,
            "projection": {},
            "filter": {
                "game_type": "regular"
            }
        }
    )

    response = requests.request("POST", url, headers=headers, data=payload)
    os.makedirs("zepor-database", exist_ok=True)
    with open(
            f"zepor-database/GameFeed_by_game_type_regular.json", "w", encoding="utf-8"
    ) as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)
