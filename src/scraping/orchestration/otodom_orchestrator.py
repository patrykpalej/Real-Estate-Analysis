import re
import time
import json
import random
from enum import Enum
from datetime import datetime

from scraping.otodom import (OtodomSearchParams,
                             OtodomLotSearchParams,
                             OtodomHouseSearchParams,
                             OtodomApartmentSearchParams)

from scraping.abstract.otodom_scraper import OtodomScraper

from scraping.otodom.otodom_lot_scraper import OtodomLotScraper
from scraping.otodom.otodom_house_scraper import OtodomHouseScraper
from scraping.otodom.otodom_apartment_scraper import OtodomApartmentScraper

from scraping.utils.general import generate_scraper_name


class FiltersPath(Enum):
    LOTS: str = "scraping/search_filters/otodom/lot_filters.json"
    HOUSES: str = "scraping/search_filters/otodom/house_filters.json"
    APARTMENTS: str = "scraping/search_filters/otodom/apartment_filters.json"


class OtodomOrchestrator:
    def __init__(self, property_type: str, scraper_name: str = None):
        self.property_type = property_type

        custom_filters_path = FiltersPath.__dict__[property_type].value
        self.search_params, self.n_pages_to_scrape \
            = self.parse_search_params(custom_filters_path)

        self.scraper = self.get_scraper(scraper_name)

    def get_default_search_params(self) -> OtodomSearchParams:
        """
        Returns a proper class with default search params
        based on property type
        """
        match self.property_type:
            case "LOTS":
                return OtodomLotSearchParams()
            case "HOUSES":
                return OtodomHouseSearchParams()
            case "APARTMENT":
                return OtodomApartmentSearchParams()

    def get_scraper(self, scraper_name: str) -> OtodomScraper:
        """
        Returns a proper scraper instance based on property type
        """
        match self.property_type:
            case "LOTS":
                return OtodomLotScraper(scraper_name)
            case "HOUSES":
                return OtodomHouseScraper(scraper_name)
            case "APARTMENT":
                return OtodomApartmentScraper(scraper_name)

    def parse_search_params(self, custom_filters_path: str) -> (dict, int):
        """
        Combines default and custom search params (filters)

        Returns:
            (dict): dict of search params
            (int): number of pages to search (or -1 for all existing pages)
        """
        default_search_params = self.get_default_search_params()

        with open(custom_filters_path, "r") as file:
            custom_search_params = json.load(file)

        search_params_dict = default_search_params.to_dict()
        search_params_dict.update(custom_search_params["filters"])

        return search_params_dict, custom_search_params["n_pages"]

    def search_offers_urls(self, cache: bool = True) -> list[str]:
        """
        Searches for offers urls based on search params and saves urls to Redis
        """
        offers_urls = self.scraper.list_offers_urls_from_search_params(
            self.search_params, self.n_pages_to_scrape)
        if cache:
            self.scraper.cache_data(self.scraper.name, offers_urls)

        return offers_urls

    def scrape_cached_urls(self,
                           cache_pattern: str,
                           clear_cache: bool = True,
                           avg_sleep_time: int = 1):
        all_keys = list(self.scraper.redis_db.scan_iter())
        matching_keys = [key
                         for key in all_keys
                         if re.match(cache_pattern, key.decode())]

        all_offers = []
        for key in matching_keys:
            urls_package = self.scraper.read_cache(key, from_json=True)
            for url in urls_package[:2]:  # TODO [:2]
                offer_data_model = self.scraper.scrape_offer_from_url(url)

                sleep_time = random.normalvariate(avg_sleep_time,
                                                  avg_sleep_time**0.5)
                time.sleep(sleep_time)

                all_offers.append(offer_data_model)

            if clear_cache:
                self.scraper.clear_cache(key)

        return all_offers


if __name__ == "__main__":
    property_type = "LOTS"
    scraper_name = generate_scraper_name(property_type)

    orchestrator = OtodomOrchestrator(property_type, scraper_name)

    offers = orchestrator.scrape_cached_urls(r"\d*-16.*",
                                             clear_cache=False,
                                             avg_sleep_time=5)
    print(offers)
