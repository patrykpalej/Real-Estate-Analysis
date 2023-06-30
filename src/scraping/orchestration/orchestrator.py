import re
import json
from dotenv import load_dotenv

from utils.general import random_sleep
from scraping.otodom import OtodomSearchParams
from utils.scraping import generate_scraper_name
from data.models.otodom import OtodomOffer
from scraping.orchestration import (OtodomFiltersPath,
                                    DomiportaFiltersPath,
                                    OtodomSearchParamsSet,
                                    DomiportaSearchParamsSet,
                                    OtodomScrapers,
                                    DomiportaScrapers)

from data.storage.manager import StorageManager


class ScrapingOrchestrator:
    def __init__(self,
                 service_name: str,
                 property_type: str,
                 scraper_name: str = None,
                 mode: int = 0):

        self.service_name = service_name
        self.property_type = property_type
        self.scraper = self._get_scraper_class()(scraper_name)
        self.storage_manager = StorageManager(self.service_name,
                                              self.property_type,
                                              mode)

    def _get_scraper_class(self) -> type:
        """
        Returns a proper scraper class
        """
        match self.service_name:
            case "OTODOM":
                return OtodomScrapers.__dict__[self.property_type].value
            case "DOMIPORTA":
                return DomiportaScrapers.__dict__[self.property_type].value
            case _:
                # TODO: raise exception
                raise Exception()

    def _get_default_search_params(self) -> OtodomSearchParams:
        """
        Returns a proper class with default search params
        based on property type
        """
        match self.service_name:
            case "OTODOM":
                return OtodomSearchParamsSet.__dict__[self.property_type].value()
            case "DOMIPORTA":
                return DomiportaSearchParamsSet.__dict__[self.property_type].value()
            case _:
                raise Exception()
                # TODO: raise error

    def _get_custom_search_params(self) -> dict:
        """
        Returns a dict with custom search parameters based on service name
        and property
        """
        match service_name:
            case "OTODOM":
                path = OtodomFiltersPath.__dict__[self.property_type].value
            case "DOMIPORTA":
                path = DomiportaFiltersPath.__dict__[self.property_type].value
            case _:
                path = None
                # TODO: raise error

        with open(path, "r") as file:
            custom_search_params = json.load(file)

        return custom_search_params

    @staticmethod
    def _combine_search_params(default_search_params: OtodomSearchParams,
                               custom_search_params: dict) -> (dict, int):
        """
        Combines default and custom search params (filters)

        Returns:
            (dict): dict of search params / filters
            (int): number of pages to search
        """
        search_params_dict = default_search_params.to_dict()
        search_params_dict.update(custom_search_params["filters"])

        return search_params_dict, custom_search_params["n_pages"]

    def search_offers_urls(self, cache: bool = True,
                           avg_sleep_time: int = 2) -> list[str]:
        """
        Searches for offers urls based on search params and saves urls to Redis
        """
        default_search_params = self._get_default_search_params()
        custom_search_params = self._get_custom_search_params()

        all_search_params, n_pages_to_scrape = self._combine_search_params(
            default_search_params, custom_search_params)

        offers_urls = self.scraper.list_offers_urls_from_search_params(
            all_search_params, n_pages_to_scrape, avg_sleep_time)

        if cache:
            cache_key_name = f"{self.scraper.name}_{len(offers_urls)}"
            self.storage_manager.cache_data(cache_key_name, offers_urls)

        return offers_urls

    def scrape_cached_urls(self,
                           cache_pattern: str,
                           clear_cache: bool = True,
                           avg_sleep_time: int = 2):
        """
        Reads cached URLs based on a given pattern and scrapes them
        """
        all_keys = self.storage_manager.redis_db.scan_iter()
        matching_keys = [key
                         for key in all_keys
                         if re.match(cache_pattern, key.decode())]

        all_offers = []
        for key in matching_keys:
            urls_package = self.storage_manager.read_cache(key, from_json=True)
            for url in urls_package[:2]:  # TODO [:2]
                random_sleep(avg_sleep_time)
                offer_data_model = self.scraper.scrape_offer_from_url(url)
                all_offers.append(offer_data_model)

            if clear_cache:
                self.storage_manager.clear_cache(key)

        return all_offers

    def store_scraped_offers(self, offers: list[OtodomOffer],
                             postgresql: bool = False,
                             mongodb: bool = False,
                             bigquery: bool = False):
        """
        Dumps scraped offers to one or many of databases
        """

        if postgresql:
            self.storage_manager.store_in_postgresql(offers)

        if mongodb:
            self.storage_manager.store_in_mongodb(offers)

        if bigquery:
            self.storage_manager.store_in_bigquery(offers)


if __name__ == "__main__":
    load_dotenv()
    # TODO: CLI - args: the following:
    service_name = "OTODOM"  # OTODOM, DOMIPORTA
    property_type = "LOTS"  # LOTS, HOUSES, APARTMENTS
    job_type = "SCRAPE"  # SEARCH, SCRAPE
    mode = 0  # 0, 1, 2
    loglevel = 30

    scraper_name = generate_scraper_name(service_name, property_type)

    orchestrator = ScrapingOrchestrator(service_name, property_type,
                                        scraper_name, mode)

    # orchestrator.search_offers_urls()

    # pattern = r"230627-1232_OTODOM_LOTS_216"
    # offers = orchestrator.scrape_cached_urls(pattern,
    #                                          clear_cache=False,
    #                                          avg_sleep_time=5)
    #
    # orchestrator.store_scraped_offers(offers,
    #                                   postgresql=False, mongodb=True)

    orchestrator.storage_manager.redis_db.close()
