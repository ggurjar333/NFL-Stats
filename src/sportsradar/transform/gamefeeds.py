from src.sportsradar import logging_helpers


logger = logging_helpers.get_logger(__name__)


class GameFeedsTransformer:
    """This class transforms game feeds into structured format"""

    def __init__(self, data: dict):
        self.data = data

    def transform_boxscore(self):
        self.data.pop("_id")
        self.data.pop("_comment")
        return self.data

    def transform_game_roster(self):
        self.data.pop("_id")
        self.data.pop("_comment")
        return self.data

    def transform_game_statistics(self):
        self.data.pop("_id")
        self.data.pop("_comment")
        return self.data
