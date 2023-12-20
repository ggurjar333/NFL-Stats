from dotenv import load_dotenv
import os
import unittest
from datetime import datetime
from src.sportsradar.extract.additionalfeeds import AdditionalFeeds
from src.sportsradar.workspace.datastore import save_data

load_dotenv('../../../../../.env')


class TestConstants:
    BASE_URL = 'https://api.sportradar.us/nfl/official'
    ACCESS_LEVEL = 'trial'
    VERSION = 'v7'
    LANGUAGE_CODE = 'en'
    FORMAT = 'json'
    API_KEY = f'{os.environ.get("APIKEY")}'
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestAdditionalFeeds(unittest.TestCase):
    def setUp(self):
        self.additionalfeeds = AdditionalFeeds(base_url=TestConstants.BASE_URL)
        self.year = datetime.now().year # 2023
        self.nfl_season = 'PST'	 # Preseason (PRE), Regular Season (REG), or Post-Season (PST).
        self.nfl_season_week = 10	# The number of weeks into the season in 2 digit format (WW).
        self.expected_status = 200

    def test_get_weekly_depth_charts(self):
        result = self.additionalfeeds.get_weekly_depth_charts(access_level=TestConstants.ACCESS_LEVEL,
                                                      language_code=TestConstants.LANGUAGE_CODE,
                                                      version=TestConstants.VERSION,
                                                      year=self.year,
                                                      nfl_season=self.nfl_season,
                                                      nfl_season_week=self.nfl_season_week,
                                                      file_format=TestConstants.FORMAT,
                                                      api_key=TestConstants.API_KEY)
        if result.status_code == self.expected_status:
            save_data(response=result,
                      db_uri=TestConstants.MONGODB_URL,
                      database=TestConstants.MONGODB_DATABASE,
                      collection=f'test_get_weekly_depth_charts_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                      )
        assert result.status_code == self.expected_status, f"Expected status code {self.expected_status}, but got {result.status_code}."
