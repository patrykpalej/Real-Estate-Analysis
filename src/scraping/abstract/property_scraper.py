import toml
import json
import redis
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from datetime import datetime

from scraping.utils.requesting import generate_random_headers


toml_config = toml.load("conf/config.toml")


class PropertyScraper(ABC):
    def __init__(self, scraper_name, service_name):
        self.name: str = str(scraper_name)
        self.service_name: str = service_name
        self.created_at: datetime = datetime.now()

        host, port, db = toml_config["redis"].values()
        self.redis_db = redis.Redis(host=host, port=port, db=db)

    def __repr__(self):
        return f"Scraper: {self.name}"

    def __str__(self):
        return f"Scraper: {self.name}"

    @abstractmethod
    def parse_offer_soup(self, offer_soup: BeautifulSoup):
        raise NotImplementedError

    @staticmethod
    def generate_headers():
        """
        Generates random headers which are stored in configuration file
        """
        return generate_random_headers()

    @staticmethod
    def request_http_get(url: str,
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
    def make_soup(http_response: requests.Response) -> BeautifulSoup:
        return BeautifulSoup(http_response.text, 'html.parser')

    def cache_data(self, key: str, data: str | list[str]):
        """
        Puts data to cache under the given key.
        If list, dict or tuple, first json.dumps() it
        """
        if isinstance(data, (str, int, float)):
            self.redis_db.set(key, data)
        elif isinstance(data, (list, dict, tuple)):
            self.redis_db.set(key, json.dumps(data))
        else:
            # TODO: warning
            pass

    def read_cache(self, key: str, from_json: bool = False):
        """
        Reads from cache under a given key and returns the value.
        If `from_json` then it json.loads() first.
        """
        value = self.redis_db.get(key)
        if from_json:
            return json.loads(value)
        else:
            return value

    def clear_cache(self, key: str) -> int:
        """
        Clears cache under a given key and returns if success
        """
        return self.redis_db.delete(key)
