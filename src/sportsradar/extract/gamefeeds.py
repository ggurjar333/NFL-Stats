import os

import requests

from sportsradar.logging_helpers

logger = sportsradar.logging_helpers.get_logger(__name__)

class GameFeeds:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_weekly_schedule(self, season_year, season_type, week_number):
        return requests.get(f'{self.base_url}/{season_year}/{season_type}/{week_number}/schedule.json?api_key={os.environ.get("APIKEY")}')
