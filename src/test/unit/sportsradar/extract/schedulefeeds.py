import os
from dotenv import load_dotenv
import unittest
from datetime import datetime
from src.sportradar.extract.schedulefeeds import ScheduleFeeds
import src.sportradar.workspace.datastore import save_data

load_dotenv('../../../../.env')


class TestConstants:
    BASE_URL = 'https://api.sportradar.us/nfl/official'
    ACCESS_LEVEL = 'trial'
    VERSION = 'v7'
    LANGUAGE_CODE = 'en'
    FORMAT = 'json'
    API_KEY = f'{os.environ("APIKEY")}'
    MONGODB_URL = f'{os.environ('MONGODB_URL')}'
    MONGODB_DATABASE = f"{os.environ('MONGO_DATABASE')}"


class TestScheduleFeeds(unittest.TestCase):
    def setUp(self):
        self.schedule_feeds = ScheduleFeeds(base_url=TestConstants,BASE_URL)

    
    def test_get_current_season_schedule(self):
        result = self.schedule_feeds.get_current_season_schedule(access_level = TestConstants.ACCESS_LEVEL,
                                                                    language_code= TestConstants.LANGUAGE_CODE,
                                                                    version= TestConstants.VERSION,
                                                                    file_format=TestConstants.file_format,
                                                                    api_key = TestConstants.API_KEY 
                                                                    )
        
        if results.status_code = self.expected_status:
            save_data(response=result,
                db_uri = TestConstants.MONGODB_URL,
                database = TestConstants.MONGO_DATABASE,
                collection =f'test_current_season_schedule_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        assert result.status_code = self.expected_status, f"Expected Status code {self.expected_status}, but got {result.status_code}."