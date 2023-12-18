import requests
from pip._internal.network.session import HTTPAdapter
# from typing import Self, Any
from urllib3.util.retry import Retry
from pydantic import HttpUrl
from requests.adapters import HTTPAdapter

# import sportsradar
import sportsradar.logging_helpers

logger = sportsradar.logging_helpers.get_logger(__name__)


class SportsRadarFetcher:
    def __init__(self, timeout: float = 15):
        self.timeout = timeout
        retries = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.http = requests.Session()
        self.http.mount("http://", adapter)
        self.http.mount("https://", adapter)
        self._descriptor_cache = {}

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
    def __init__(self, sports_radar_fetcher):
        self.sports_radar_fetcher = sports_radar_fetcher

    def fetch_data(self, url):
        return self.sports_radar_fetcher.fetch_data(url)


from datastore import SportsRadarFetcher, DataStore

# Create a SportsRadarFetcher instance
sports_radar_fetcher = SportsRadarFetcher()

# Pass the instance to DataStore
data_store = DataStore(sports_radar_fetcher)

# Fetch data from a specific URL
url_to_fetch = 'http://example.com'  # replace with your actual URL
data = data_store.fetch_data(url_to_fetch)

print(data.status_code, data.text)  # prints the status code and content of the response