from src.sportsradar import logging_helpers
from src.sportsradar.transform.classes import DataPreprocessor
from src.sportsradar.transform.params.teamfeeds import remove_unwanted_feeds

logger = logging_helpers.get_logger(__name__)


class TeamFeedsTransformer:
    """
    TeamFeedsTransformer class is used to transform team feeds data.

    Args:
        data (dict): A dictionary containing team roster data.

    Methods:
        transform_team_roster(): Transforms the team roster data by removing unwanted feeds.

    Returns:
        dict: The transformed team roster data.
    """

    def __init__(self, data: dict):
        self.data = data

    def transform_team_roster(self):
        preprocessor = DataPreprocessor(
            data=self.data, processor=remove_unwanted_feeds()
        )
        return preprocessor.data

    def transform_seasonal_statistics(self):
        preprocessor = DataPreprocessor(
            data=self.data, processor=remove_unwanted_feeds()
        )
        return preprocessor.data
