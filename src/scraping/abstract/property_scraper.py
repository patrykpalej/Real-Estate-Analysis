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
        return self

    def __str__(self):
        return self

    @abstractmethod
    def parse_offer_soup(self, offer_soup: BeautifulSoup):
        raise NotImplementedError

    @staticmethod
    def generate_headers():
        return generate_random_headers()

    @staticmethod
    def request_http_get(url: str,
                         headers: dict = None,
                         params: dict = None) -> requests.Response:

        response = requests.get(url,
                                headers=headers,
                                params=params)
        return response

    @staticmethod
    def make_soup(http_response: requests.Response) -> BeautifulSoup:
        return BeautifulSoup(http_response.text, 'html.parser')

    def cache_data(self, key: str, data: str | list[str]):
        if isinstance(data, (str, int, float)):
            self.redis_db.set(key, data)
        elif isinstance(data, (list, dict, tuple)):
            self.redis_db.set(key, json.dumps(data))
        else:
            # TODO: warning
            pass

    def uncache_data(self, key: str, from_json: bool = False):
        value = self.redis_db.get(key)
        if from_json:
            return json.loads(value)
        else:
            return value
