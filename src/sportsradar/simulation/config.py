import os
from dotenv import load_dotenv

load_dotenv("../../../.env")


class Config:
    BASE_URL = "https://playback.sportradar.com"
    CONTENT_TYPE = "json"
    LEAGUE = "nfl"
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
