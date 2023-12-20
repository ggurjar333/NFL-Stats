from dotenv import load_dotenv
import os
from src.sportsradar.extract.gamefeeds import GameFeeds
from src.sportsradar.workspace.datastore import DataStore

load_dotenv('../../../../../.env')


class TestConstants():
    BASE_URL = 'https://api.sportradar.us/nfl/official'
    ACCESS_LEVEL = 'trial'
    VERSION = 'v7'
    LANGUAGE_CODE = 'en'
    FORMAT = 'json'
    API_KEY = f'{os.environ.get("APIKEY")}'


import unittest


class TestGameFeeds(unittest.TestCase):
    def setUp(self):
        self.game_feeds = GameFeeds(base_url=TestConstants.BASE_URL)
        self.game_id = '251ac0cf-d97d-4fe8-a39e-09fc4a95a0b2'
        self.expected_status = 200

    def test_get_game_boxscore(self):
        result = self.game_feeds.get_game_boxscore(access_level=TestConstants.ACCESS_LEVEL,
                                                   language_code=TestConstants.LANGUAGE_CODE,
                                                   version=TestConstants.VERSION,
                                                   game_id=self.game_id,
                                                   file_format=TestConstants.FORMAT,
                                                   api_key=TestConstants.API_KEY)
        assert result.status_code == self.expected_status, f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_game_roster(self):
        # Execute
        game_feeds = GameFeeds(base_url=TestConstants.BASE_URL)
        game_id = '251ac0cf-d97d-4fe8-a39e-09fc4a95a0b2'
        result = game_feeds.get_game_roster(access_level=TestConstants.ACCESS_LEVEL,
                                            language_code=TestConstants.LANGUAGE_CODE, version=TestConstants.VERSION,
                                            game_id=game_id, file_format=TestConstants.FORMAT,
                                            api_key=TestConstants.API_KEY)
        assert result.status_code == self.expected_status, f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_game_statistics(self):
        # Execute
        game_feeds = GameFeeds(base_url=TestConstants.BASE_URL)
        game_id = '251ac0cf-d97d-4fe8-a39e-09fc4a95a0b2'
        result = game_feeds.get_game_statistics(access_level=TestConstants.ACCESS_LEVEL,
                                                language_code=TestConstants.LANGUAGE_CODE,
                                                version=TestConstants.VERSION,
                                                game_id=game_id, file_format=TestConstants.FORMAT,
                                                api_key=TestConstants.API_KEY)
        assert result.status_code == self.expected_status, f"Expected status code {self.expected_status}, but got {result.status_code}."


if __name__ == '__main__':
    unittest.main()
