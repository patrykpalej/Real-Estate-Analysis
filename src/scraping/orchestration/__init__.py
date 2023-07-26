from enum import Enum

from scraping.otodom import (OtodomSearchParams,
                             OtodomLotSearchParams,
                             OtodomHouseSearchParams,
                             OtodomApartmentSearchParams)

from scraping.abstract.otodom_scraper import OtodomScraper
from scraping.otodom.otodom_lot_scraper import OtodomLotScraper
from scraping.otodom.otodom_house_scraper import OtodomHouseScraper
from scraping.otodom.otodom_apartment_scraper import OtodomApartmentScraper


# Filter paths Enums
class OtodomFiltersPath(Enum):
    LOTS: str = "../src/conf/scraping/search_filters/otodom/lot_filters.json"
    HOUSES: str = "../src/conf/scraping/search_filters/otodom/house_filters.json"
    APARTMENTS: str = "../src/conf/scraping/search_filters/otodom/apartment_filters.json"


class DomiportaFiltersPath(Enum):
    pass


# Search params Enums
class OtodomSearchParamsSet(Enum):
    LOTS: OtodomSearchParams = OtodomLotSearchParams
    HOUSES: OtodomSearchParams = OtodomHouseSearchParams
    APARTMENTS: OtodomSearchParams = OtodomApartmentSearchParams


class DomiportaSearchParamsSet(Enum):
    pass


# Scrapers Enums
class OtodomScrapers(Enum):
    LOTS: OtodomScraper = OtodomLotScraper
    HOUSES: OtodomScraper = OtodomHouseScraper
    APARTMENTS: OtodomScraper = OtodomApartmentScraper


class DomiportaScrapers(Enum):
    pass


# Job types Enum
class JobTypes(Enum):
    SEARCH: str = "SEARCH"
    SCRAPE: str = "SCRAPE"
