import requests
from bs4 import BeautifulSoup
from types import MappingProxyType
from abc import ABC, abstractmethod
from datetime import datetime

from scrapers.utils.requesting import generate_random_headers


class PropertyScraper(ABC):
    def __init__(self, scraper_name, service_name):
        self.name = scraper_name
        self.service_name = service_name
        self.created_at = datetime.now()

    def __repr__(self):
        return self

    def __str__(self):
        return self

    @abstractmethod
    def parse_soup(self):
        raise NotImplementedError

    @staticmethod
    def _generate_headers():
        return generate_random_headers()

    @staticmethod
    def request_http(url: str,
                     headers: MappingProxyType = None,
                     params: MappingProxyType = None):

        response = requests.get(url,
                                headers=headers,
                                params=params)

        return response

    @staticmethod
    def make_soup(http_response: requests.Response):
        return BeautifulSoup(http_response.text, 'html.parser')

    def cache_data(self):
        pass

    def uncache_data(self):
        pass


