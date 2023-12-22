from src.sportsradar import logging_helpers


logger = logging_helpers.get_logger(__name__)


class GameFeedsTransformer:
    """

    Class: GameFeedsTransformer

    This class is responsible for transforming game feeds data by removing unwanted keys.

    Attributes:
    - UNWANTED_KEYS: A list of keys that are unwanted and should be removed from the data.

    Methods:
    - __init__(self, data: dict): Initializes an instance of the GameFeedsTransformer class with the provided data.
    - _remove_unwanted_keys(): Removes the unwanted keys from the data.
    - transform_boxscore(): Transforms the game feeds data for boxscore.
    - transform_game_roster(): Transforms the game feeds data for game roster.
    - transform_game_statistics(): Transforms the game feeds data for game statistics.

    """

    UNWANTED_KEYS = ["_comment"]

    def __init__(self, data: dict):
        self.data = data

    def _remove_unwanted_keys(self):
        for key in self.UNWANTED_KEYS:
            if key in self.data:
                self.data.pop(key)

    def transform_boxscore(self):
        self._remove_unwanted_keys()
        return self.data

    def transform_game_roster(self):
        self._remove_unwanted_keys()
        return self.data

    def transform_game_statistics(self):
        self._remove_unwanted_keys()
        return self.data
