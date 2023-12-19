import os
import unittest
from unittest.mock import patch, Mock
from src.sportsradar.extract.gamefeeds import GameFeeds


# 'http://api.sportradar.us/nfl/official/trial/v7/en/games/{season_year}/{season_type}/{week_number}/schedule.json?api_key={API_KEY}'

class TestGameFeeds(unittest.TestCase):
    """Unit tests for GameFeeds class."""

    @classmethod
    def setUpClass(cls):
        """Set up for all tests."""
        cls.game_feeds = GameFeeds("http://api.sportradar.us/nfl/official/trial/v7/en/games")

    @patch('requests.get', autospec=True)
    def test_get_weekly_schedule(self, mock_get):
        """Test get_weekly_schedule method."""
        # Arrange
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"arbitrary": "test_data"}
        mock_get.return_value = mock_resp
        season_year = '2023'
        season_type = 'preseason'
        week_number = '3'
        api_key = os.getenv('API_KEY')  # Obtain the API key from an environment variable
        # Act
        result = self.game_feeds.get_weekly_schedule(season_year, season_type, week_number)
        # Assert
        mock_get.assert_called_with(
            f"http://api.sportradar.us/nfl/official/trial/v7/en/games{season_year}/{season_type}/{week_number}/schedule.json?api_key={api_key}"
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(mock_resp.status_code, 200)


# Instruct Python unittest framework to generate a test suite and run the tests.
if __name__ == "__main__":
    unittest.main()
