from enum import Enum

from scraping.otodom import (OtodomSearchParams,
                             OtodomLotSearchParams,
                             OtodomHouseSearchParams,
                             OtodomApartmentSearchParams)

from scraping.domiporta import (DomiportaSearchParams,
                                DomiportaLotSearchParams,
                                DomiportaHouseSearchParams,
                                DomiportaApartmentSearchParams)

from scraping.abstract.otodom_scraper import OtodomScraper
from scraping.abstract.domiporta_scraper import DomiportaScraper

from scraping.otodom.otodom_lot_scraper import OtodomLotScraper
from scraping.otodom.otodom_house_scraper import OtodomHouseScraper
from scraping.otodom.otodom_apartment_scraper import OtodomApartmentScraper

from scraping.domiporta.domiporta_lot_scraper import DomiportaLotScraper
from scraping.domiporta.domiporta_house_scraper import DomiportaHouseScraper
from scraping.domiporta.domiporta_apartment_scraper import DomiportaApartmentScraper


# Filter paths Enums
class OtodomFiltersPath(Enum):
    LOTS: str = "../src/conf/scraping/search_filters/otodom/lot_filters.json"
    HOUSES: str = "../src/conf/scraping/search_filters/otodom/house_filters.json"
    APARTMENTS: str = "../src/conf/scraping/search_filters/otodom/apartment_filters.json"


class DomiportaFiltersPath(Enum):
    LOTS: str = "../src/conf/scraping/search_filters/domiporta/lot_filters.json"
    HOUSES: str = "../src/conf/scraping/search_filters/domiporta/house_filters.json"
    APARTMENTS: str = "../src/conf/scraping/search_filters/domiporta/apartment_filters.json"


# Search params Enums
class OtodomSearchParamsSet(Enum):
    LOTS: OtodomSearchParams = OtodomLotSearchParams
    HOUSES: OtodomSearchParams = OtodomHouseSearchParams
    APARTMENTS: OtodomSearchParams = OtodomApartmentSearchParams


class DomiportaSearchParamsSet(Enum):
    LOTS: DomiportaSearchParams = DomiportaLotSearchParams
    HOUSES: DomiportaSearchParams = DomiportaHouseSearchParams
    APARTMENTS: DomiportaSearchParams = DomiportaApartmentSearchParams


# Scrapers Enums
class OtodomScrapers(Enum):
    LOTS: OtodomScraper = OtodomLotScraper
    HOUSES: OtodomScraper = OtodomHouseScraper
    APARTMENTS: OtodomScraper = OtodomApartmentScraper


class DomiportaScrapers(Enum):
    LOTS: DomiportaScraper = DomiportaLotScraper
    HOUSES: DomiportaScraper = DomiportaHouseScraper
    APARTMENTS: DomiportaScraper = DomiportaApartmentScraper


# Job types Enum
class JobTypes(Enum):
    SEARCH: str = "SEARCH"
    SCRAPE: str = "SCRAPE"
