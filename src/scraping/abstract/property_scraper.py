import toml
import logging
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from datetime import datetime

from utils.scraping import generate_random_headers


toml_config = toml.load("../src/conf/config.toml")


class PropertyScraper(ABC):
    def __init__(self, scraper_name: str):
        """
        Creates a scraper based on its name
        """
        self.name: str = scraper_name
        self.created_at: datetime = datetime.now()
        self._log = logging.getLogger(scraper_name)

    def __repr__(self):
        return f"Scraper: {self.name}"

    def __str__(self):
        return f"Scraper: {self.name}"

    @abstractmethod
    def _parse_offer_soup(self, offer_soup: BeautifulSoup):
        raise NotImplementedError

    @staticmethod
    def _generate_headers():
        """
        Generates random headers which are stored in configuration file
        """
        return generate_random_headers()

    def _request_http_get(self,
                          url: str,
                          headers: dict = None,
                          params: dict = None) -> requests.Response:
        """
        Sends a get request under the given URL with headers (if exist)
        and params (if exist). Returns the response.
        """
        try:
            response = requests.get(url,
                                    headers=headers,
                                    params=params)
        except Exception as e:
            self._log.error(f"Requesting {url} failed")
            self._log.exception(e)
            return requests.Response()

        if not response.ok:
            self._log.warning(f"Response code {response.status_code} when"
                              f" requesting {url}")

        return response

    def _make_soup(self, http_response: requests.Response) -> BeautifulSoup:
        try:
            return BeautifulSoup(http_response.text, 'html.parser')
        except Exception as e:
            self._log.error("Making soup failed")
            self._log.exception(e)
            return BeautifulSoup("", 'html.parser')
