import json
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


if __name__ == "__main__":
    property_type = "LOTS"
    scraper_name = datetime.now().strftime("%y%m%d-%H%M") + "_" + property_type

    orchestrator = OtodomOrchestrator(property_type, scraper_name)
    _ = orchestrator.search_offers_urls()

    data = orchestrator.scraper.read_cache("230625-1701_LOTS",
                                           from_json=True)
    print(len(data))
    print(data)
