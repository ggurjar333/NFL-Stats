import requests
from pip._internal.network.session import HTTPAdapter
# from typing import Self, Any
from urllib3.util.retry import Retry
from pydantic import HttpUrl
from requests.adapters import HTTPAdapter

# import sportsradar
from src.sportsradar import logging_helpers

logger = logging_helpers.get_logger(__name__)


class SportsRadarFetcher:
    """
    This class is responsible for fetching
     data from SportsRadar.


    Attributes:
        timeout (float): The timeout value
          for HTTP requests.
        http (requests.Session): The HTTP
          session to use for requests.
    """
    def __init__(self, timeout: float = 15):
        """
        Constructs a new 'SportsRadarFetcher'
          object.
        :param timeout: The timeout value for
           HTTP requests.
        :return: returns nothing
        """
        self.timeout = timeout
        retries = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.http = requests.Session()
        self.http.mount("http://", adapter)
        self.http.mount("https://", adapter)

    def _fetch_from_url(self, url: HttpUrl) -> requests.Response:
        """
        Fetches data from from a given URL.

        :param url: The URL to fetch data from
          from.
        :return: The response from the HTTP
          request.
        """
        logger.info(f"Retrieving {url} from SportsRadar")
        response = self.http.get(url, timeout=self.timeout)
        if response.status_code == requests.codes.ok:
            logger.debug(f"Successfully downloaded from {url}")
            return response
        raise ValueError(f"Could not download from {url}: {response.text}")

    def fetch_data(self, url: HttpUrl) -> requests.Response:
        return self._fetch_from_url(url)


class DataStore:
    """
    This class uses SportsRadarFetcher to fetch data.

    Attributes:
        sports_radar_fetcher (SportsRadarFetcher): The SportsRadarFetcher instance to use for fetching data.
    """
    def __init__(self, sports_radar_fetcher):
        """
        Constructs a new 'DataStore' object.

        :param sports_radar_fetcher: The SportsRadarFetcher instance.
        :return: returns nothing
        """
        self.sports_radar_fetcher = sports_radar_fetcher

    def fetch_data(self, url):
        """
        Fetches data from a given URL using the SportsRadarFetcher instance.

        :param url: The URL to fetch data from.
        :return: The response from the HTTP request.
        """

        return self.sports_radar_fetcher.fetch_data(url)