import requests
from urllib3.util.retry import Retry
from pydantic import HttpUrl
from requests.adapters import HTTPAdapter

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
        self.timeout = timeout
        retries = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.http = requests.Session()
        self.http.mount("http://", adapter)
        self.http.mount("https://", adapter)

    def _fetch_from_url(self, url: HttpUrl) -> requests.Response:
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
    This class used to fetch data.

    Attributes:
        datakeeper (SportsRadarFetcher): The instance to use for fetching data.
    """

    def __init__(self, datakeeper):
        self.datakeeper = datakeeper

    def fetch_data(self, url):
        return self.datakeeper.fetch_data(url)