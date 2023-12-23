from src.sportsradar import logging_helpers
from src.sportsradar.transform.classes import DataPreprocessor
from src.sportsradar.transform.params.gamefeeds import remove_unwanted_feeds

logger = logging_helpers.get_logger(__name__)


class GameFeedsTransformer:
    """
    Class to transform game feeds data.

    Attributes:
        UNWANTED_KEYS (list): List of unwanted keys to be removed from the data dictionary.

    Args:
        data (dict): The game feeds data dictionary.

    Methods:
        transform_boxscore: Transforms the boxscore data.
        transform_game_roster: Transforms the game roster data.
        transform_game_statistics: Transforms the game statistics data.
    """

    def __init__(self, data: dict):
        self.data = data

    def transform_boxscore(self):
        preprocessor = DataPreprocessor(
            data=self.data, processor=remove_unwanted_feeds()
        )
        return preprocessor.data

    def transform_game_roster(self):
        preprocessor = DataPreprocessor(
            data=self.data, processor=remove_unwanted_feeds()
        )
        return preprocessor.data

    def transform_game_statistics(self):
        preprocessor = DataPreprocessor(
            data=self.data, processor=remove_unwanted_feeds()
        )
        return preprocessor.data
