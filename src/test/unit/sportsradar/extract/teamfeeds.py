from dotenv import load_dotenv
import os
import unittest
from datetime import datetime
from src.sportsradar.extract.teamfeeds import TeamFeeds
from src.sportsradar.workspace.datastore import save_data

load_dotenv("../../../../../.env")


class TestConstants:
    BASE_URL = "https://api.sportradar.us/nfl/official"
    ACCESS_LEVEL = "trial"
    VERSION = "v7"
    LANGUAGE_CODE = "en"
    FORMAT = "json"
    API_KEY = f'{os.environ.get("APIKEY")}'
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestTeamFeeds(unittest.TestCase):
    def setUp(self):
        self.team_feeds = TeamFeeds(base_url=TestConstants.BASE_URL)
        self.team_id = "ce92bd47-93d5-4fe9-ada4-0fc681e6caa0"
        self.expected_status = 200

    def test_get_team_roster(self):
        result = self.team_feeds.get_team_roster(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            team_id=self.team_id,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_team_roster_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestTeamFeeds")
