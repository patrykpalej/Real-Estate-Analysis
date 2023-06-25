import json
from abc import ABC, abstractmethod
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from scraping.abstract.property_scraper import PropertyScraper
from scraping import Services
from scraping.otodom import OtodomSearchParams


class OtodomScraper(PropertyScraper, ABC):
    SERVICE_NAME: str = Services.OTODOM.value
    BASE_URL: str = "https://www.otodom.pl/"
    OFFER_BASE_URL: str = "https://www.otodom.pl/pl/oferta/"
    SUB_URL: None

    def __init__(self, scraper_name: str):
        super().__init__(scraper_name, self.SERVICE_NAME)

    @abstractmethod
    def parse_offer_soup(self, offer_soup: BeautifulSoup):
        raise NotImplementedError

    def get_offers_urls_from_search_soup(
            self, search_soup: BeautifulSoup, n_pages=None) -> list[str]:
        all_scripts = search_soup.find_all("script",
                                           {"type": "application/json"})
        offers_script_idx = 0
        try:
            offers_json = json.loads(all_scripts[offers_script_idx].text)
        except json.decoder.JSONDecodeError:
            # TODO: warning - no offers found
            return []
        offers_list = (offers_json["props"]["pageProps"]["data"]
                       ["searchAds"]["items"])
        offers_slugs = [offer["slug"] for offer in offers_list]
        offers_urls = [self.OFFER_BASE_URL + slug for slug in offers_slugs]

        # TODO: scrape urls from all pages (if None) or n_pages
        return offers_urls

    @staticmethod
    def get_offer_data_from_offer_soup(offer_soup: BeautifulSoup) -> dict:
        offer_data = offer_soup.find("script", {"id": "__NEXT_DATA__"}).text
        offer_full_json = json.loads(offer_data)
        offer_json = offer_full_json["props"]["pageProps"]["ad"]
        return offer_json

    def list_offers_urls_from_search_params(
            self, search_params: dict) -> list[str]:
        random_headers = self.generate_headers()
        search_url = urljoin(self.BASE_URL, self.SUB_URL)

        search_response = self.request_http_get(search_url,
                                                headers=random_headers,
                                                params=search_params)
        search_soup = self.make_soup(search_response)
        urls_list = self.get_offers_urls_from_search_soup(search_soup)

        return urls_list

    def scrape_offer_from_url(self, url: str) -> str:
        random_headers = self.generate_headers()
        response = self.request_http_get(url,
                                         headers=random_headers)
        offer_soup = self.make_soup(response)
        offer_data = self.parse_offer_soup(offer_soup)
        return offer_data


if __name__ == "__main__":
    pass
