import os
import unittest
from dotenv import load_dotenv


load_dotenv("../../../.env")


class TestConstants:
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class DraftFeedsTransformer(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dummy_data = {
            "home_team": "Team A",
            "away_team": "Team B",
            "_comment": "10-5",
        }
        self.gft = DraftFeedsTransformer(self.dummy_data)

    def test_transform_draft_summary(self):
        # Act
        result = self.gft.transform_draft_summary()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_prospects(self):
        # Act
        result = self._remove_unwanted_feeds()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_team_draft_summary(self):
        # Act
        result = self._remove_unwanted_feeds()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_top_prospects(self):
        # Act
        result = self._remove_unwanted_feeds()

        # assert
        self.assertIsInstance(result, dict)

    def test_transform_trades(self):
        # Act
        result = self._remove_unwanted_feeds()

        # assert
        self.assertIsInstance(result, dict)
