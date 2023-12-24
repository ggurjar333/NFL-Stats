from src.sportsradar import logging_helpers

logger = logging_helpers.get_logger(__name__)


class DraftFeedsTransformer:
    """
    DraftFeedsTransformer class is used to transform draft feeds data.

    Args:
        data (dict): A dictionary containing draft feeds data.

    Methods:
        transform_weekly_depth_charts(): Transforms the weekly depth charts data by removing unwanted feeds.

    Returns:
        dict: The transformed team weekly depth charts.
    """

    UNWANTED_KEYS = ["_comment"]

    def __init__(self, data: dict):
        self.data = data

    def _remove_unwanted_feeds(self):
        for key in self.UNWANTED_KEYS:
            if key in self.data:
                self.data.pop(key)

    def transform_draft_summary(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_prospects(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_team_draft_summary(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_top_prospects(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_trades(self):
        self._remove_unwanted_feeds()
        return self.data
