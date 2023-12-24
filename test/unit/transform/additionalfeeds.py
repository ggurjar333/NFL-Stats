import os
import unittest
from dotenv import load_dotenv

from src.sportsradar.transform.additionalfeeds import AdditionalFeedsTransformer

load_dotenv("../../../.env")


class TestConstants:
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestAdditionalFeedsTransformer(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dummy_data = {
            "home_team": "Team A",
            "away_team": "Team B",
            "_comment": "10-5",
        }
        self.gft = AdditionalFeedsTransformer(self.dummy_data)

    def test_transform_weekly_depth_charts(self):
        # Act
        result = self.gft.transform_weekly_depth_charts()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_daily_change_log(self):
        # Act
        result = self.gft.transform_daily_change_log()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_daily_transactions(self):
        # Act
        result = self.gft.transform_daily_transactions()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_seasoms(self):
        # Act
        result = self.gft.transform_seasons()

        # Assert
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestAdditionalFeedsTransformer")
