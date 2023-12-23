from src.sportsradar import logging_helpers
from src.sportsradar.transform.classes import DataPreprocessor
from src.sportsradar.transform.params.playerfeeds import remove_unwanted_feeds

logger = logging_helpers.get_logger(__name__)


class PlayerFeedsTransformer:
    """
    PlayerFeedsTransformer class is used to transform player profile data.

    Args:
        data (dict): A dictionary containing player profile data.

    Methods:
        transform_player_profile(): Transforms the player profile data by removing unwanted feeds.

    Returns:
        dict: The transformed player profile data.
    """

    def __init__(self, data: dict):
        self.data = data

    def transform_player_profile(self):
        preprocessor = DataPreprocessor(
            data=self.data, processor=remove_unwanted_feeds()
        )
        return preprocessor.data
