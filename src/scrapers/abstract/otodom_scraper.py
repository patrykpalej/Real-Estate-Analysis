import json
from abc import ABC, abstractmethod
from types import MappingProxyType
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from scrapers.abstract.property_scraper import PropertyScraper


class OtodomScraper(PropertyScraper, ABC):
    SERVICE_NAME: str = "OTODOM"
    BASE_URL: str = "https://www.otodom.pl/"
    SUB_URL: None

    def __init__(self, scraper_name: str):
        super().__init__(scraper_name, self.SERVICE_NAME)

    @abstractmethod
    def parse_soup(self):
        raise NotImplementedError

    def list_offers_urls_from_search(self, search_dict: dict) -> list[str]:
        search_dict = MappingProxyType(search_dict)
        random_headers = self._generate_headers()

        search_url = urljoin(self.BASE_URL, self.SUB_URL)

        search_response = self.request_http(search_url, headers=random_headers,
                                            params=search_dict)
        search_soup = self.make_soup(search_response)
        urls_list = self.__get_offers_urls_from_search_result(search_soup)

        return urls_list

    def scrape_offer_from_url(self, url: str) -> str:
        pass

    @staticmethod
    def __get_offers_urls_from_search_result(search_soup: BeautifulSoup):
        all_scripts = search_soup.find_all("script")
        offers_script_idx = 0
        offers_json = json.loads(all_scripts[offers_script_idx].text)
        offers_list = offers_json["@graph"][2]["offers"]["offers"]
        offers_urls = [offer["url"]
                       for offer in offers_list]

        return offers_urls

    # @property
    # def search_sub_url(self):
    #     return self.SUB_URL


if __name__ == "__main__":
    pass
    # import os
    # print(os.getenv("PYTHONPATH"))
    # print(PropertyScraper)

    # from scrapers.utils.requesting import generate_random_headers
    # h = generate_random_headers()
    # print(h)
