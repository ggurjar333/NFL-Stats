from src.sportsradar import logging_helpers
from src.sportsradar.transform.classes import DataPreprocessor
from src.sportsradar.transform.params.additionalfeeds import remove_unwanted_feeds

logger = logging_helpers.get_logger(__name__)


class AdditionalFeedsTransformer:
    """
    AdditionalFeedsTransformer class is used to transform additional feeds data.

    Args:
        data (dict): A dictionary containing additional feeds data.

    Methods:
        transform_weekly_depth_charts(): Transforms the weekly depth charts data by removing unwanted feeds.

    Returns:
        dict: The transformed team weekly depth charts.
    """

    def __init__(self, data: dict):
        self.data = data

    def transform_weekly_depth_charts(self):
        preprocessor = DataPreprocessor(
            data=self.data, processor=remove_unwanted_feeds()
        )
        return preprocessor.data
