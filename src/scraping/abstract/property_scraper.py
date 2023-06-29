import toml
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from datetime import datetime

from utils.scraping import generate_random_headers


toml_config = toml.load("../src/conf/config.toml")


class PropertyScraper(ABC):
    def __init__(self, scraper_name: str, service_name: str, property_type: str):
        """
        Creates a scraper based on its name and service name
        """
        self.name: str = scraper_name
        self.service_name: str = service_name.upper()
        self.property_type: str = property_type.upper()
        self.created_at: datetime = datetime.now()

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

    @staticmethod
    def _request_http_get(url: str,
                          headers: dict = None,
                          params: dict = None) -> requests.Response:
        """
        Sends a get request under the given URL with headers (if exist)
        and params (if exist). Returns the response.
        """
        response = requests.get(url,
                                headers=headers,
                                params=params)
        return response

    @staticmethod
    def _make_soup(http_response: requests.Response) -> BeautifulSoup:
        return BeautifulSoup(http_response.text, 'html.parser')
