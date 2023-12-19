from unittest.mock import patch, Mock
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

@patch('os.getenv', return_value=TestConstants.API_KEY)
@patch('src.sportsradar.extract.gamefeeds.GameFeeds')
def test_game_feeds_with_api_key(mock_data_store, mock_getenv):

    # Execute
    game_feeds = GameFeeds(base_url=TestConstants.BASE_URL)
    game_id = '251ac0cf-d97d-4fe8-a39e-09fc4a95a0b2'
    result = game_feeds.get_game_boxscore(access_level=TestConstants.ACCESS_LEVEL, language_code=TestConstants.LANGUAGE_CODE, version=TestConstants.VERSION, game_id=game_id, file_format=TestConstants.FORMAT, api_key=TestConstants.API_KEY)
    # Check
    assert result.status_code == 200

