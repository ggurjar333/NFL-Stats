import os
import unittest
from unittest.mock import patch, MagicMock
from src.sportsradar.extract.gamefeeds import GameFeeds

class TestGameFeeds(unittest.TestCase):
    """Unit tests for GameFeeds class."""
    @classmethod
    def setUpClass(cls):
        """Set up for all tests."""
        cls.game_feeds = GameFeeds("https://testurl.com/api")

    @patch('src.sportsradar.extract.gamefeeds.DataStore', autospec=True)
    def test_get_weekly_schedule(self, mock_data_store):
        """Test get_weekly_schedule method."""
        # Arrange
        mock_data_store_instance = mock_data_store.return_value
        mock_data_store_instance.fetch_data.return_value = {"data": "test_data"}

        # Act
        result = self.game_feeds.get_weekly_schedule('2023', 'preseason', 3)

        # Assert
        mock_data_store.assert_called_once()
        mock_data_store_instance.fetch_data.assert_called_once_with(
            url="https://testurl.com/api/2023/preseason/3")
        self.assertEqual(result, {"data": "test_data"})

# Instruct Python unittest framework to generate a test suite and run the tests.
if __name__ == "__main__":
    unittest.main()