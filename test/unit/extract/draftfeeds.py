from dotenv import load_dotenv
import os
import unittest
from datetime import datetime
from src.sportsradar.extract.draftfeeds import DraftsFeeds
from src.sportsradar.workspace.datastore import save_data

load_dotenv("../../../.env")


class TestConstants:
    BASE_URL = "https://api.sportradar.us/draft/nfl"
    ACCESS_LEVEL = "trial"
    VERSION = "v1"
    LANGUAGE_CODE = "en"
    FILE_FORMAT = "json"
    API_KEY = f'{os.environ.get("APIKEY")}'
    MONGODB_URL = f'{os.environ.get("MONGODB_URL")}'
    MONGODB_DATABASE = f'{os.environ.get("MONGODB_DATABASE")}'


class TestDraftFeeds(unittest.TestCase):
    def setUp(self):
        self.draftfeeds = DraftsFeeds(base_url=TestConstants.BASE_URL)
        self.year = datetime.now().year - 2
        self.expected_status = 200

    def test_get_draft_summary(self):
        result = self.draftfeeds.get_draft_summary(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            year=self.year,
            file_format=TestConstants.FILE_FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_get_draft_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_prospects(self):
        result = self.draftfeeds.get_prospects(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            year=self.year,
            file_format=TestConstants.FILE_FORMAT,
            api_key=TestConstants.API_KEY,
        )

        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_get_prospects {datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestDraftFeeds")
