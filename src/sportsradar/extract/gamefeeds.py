import os

from src.sportsradar import logging_helpers
from src.sportsradar.workspace.datastore import DataStore, SportsRadarFetcher

logger = logging_helpers.get_logger(__name__)


class GameFeeds():
    """ This class is responsible for extracting game feeds from SportsRadar"""
    def __init__(self, base_url):
        """
        Initialize an instance of the class.

        :param base_url: The base URL for the API.
        :type base_url: str
        """
        self.base_url = base_url

    def get_game_boxscore(self, access_level, version, language_code, game_id, file_format):
        """
        Get the game boxscore for a given game_id
        :param access_level:
        :param version:
        :param language_code:
        :param game_id:
        :param file_format:
        :return: The game boxscore for the given game_id
        """
        datastore = DataStore(datakeeper=SportsRadarFetcher())
        return datastore.fetch_data(url=f"{self.base_url}/{access_level}/{version}/{language_code}/games/{game_id}/boxscore.{file_format}?api_key={os.environ.get('NFL_API_KEY')}")

    def get_weekly_schedule(self, season_year, season_type, week_number):
        """
        Get the weekly schedule for a specific season, season type, and week number.

        :param season_year: The year of the season.
        :param season_type: The type of the season (e.g., current, postseason).
        :param week_number: The week number for which to retrieve the schedule.
        :return: The weekly schedule data.
        """
        datastore = DataStore(datakeeper=SportsRadarFetcher())
        return datastore.fetch_data(url=f"{self.base_url}/{season_year}/{season_type}/{week_number}")
