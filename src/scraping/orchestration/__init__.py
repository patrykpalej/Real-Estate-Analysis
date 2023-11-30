from enum import Enum

from scraping.otodom import (OtodomSearchParams,
                             OtodomLandSearchParams,
                             OtodomHouseSearchParams,
                             OtodomApartmentSearchParams)

from scraping.domiporta import (DomiportaSearchParams,
                                DomiportaLandSearchParams,
                                DomiportaHouseSearchParams,
                                DomiportaApartmentSearchParams)

from scraping.abstract.otodom_scraper import OtodomScraper
from scraping.abstract.domiporta_scraper import DomiportaScraper

from scraping.otodom.otodom_land_scraper import OtodomLandScraper
from scraping.otodom.otodom_house_scraper import OtodomHouseScraper
from scraping.otodom.otodom_apartment_scraper import OtodomApartmentScraper

from scraping.domiporta.domiporta_land_scraper import DomiportaLandScraper
from scraping.domiporta.domiporta_house_scraper import DomiportaHouseScraper
from scraping.domiporta.domiporta_apartment_scraper import DomiportaApartmentScraper


# Filter paths Enums
class OtodomFiltersPath(Enum):
    LANDS: str = "../src/conf/scraping/search_filters/otodom/land_filters.json"
    HOUSES: str = "../src/conf/scraping/search_filters/otodom/house_filters.json"
    APARTMENTS: str = "../src/conf/scraping/search_filters/otodom/apartment_filters.json"


class DomiportaFiltersPath(Enum):
    LANDS: str = "../src/conf/scraping/search_filters/domiporta/land_filters.json"
    HOUSES: str = "../src/conf/scraping/search_filters/domiporta/house_filters.json"
    APARTMENTS: str = "../src/conf/scraping/search_filters/domiporta/apartment_filters.json"


# Search params Enums
class OtodomSearchParamsSet(Enum):
    LANDS: OtodomSearchParams = OtodomLandSearchParams
    HOUSES: OtodomSearchParams = OtodomHouseSearchParams
    APARTMENTS: OtodomSearchParams = OtodomApartmentSearchParams


class DomiportaSearchParamsSet(Enum):
    LANDS: DomiportaSearchParams = DomiportaLandSearchParams
    HOUSES: DomiportaSearchParams = DomiportaHouseSearchParams
    APARTMENTS: DomiportaSearchParams = DomiportaApartmentSearchParams


# Scrapers Enums
class OtodomScrapers(Enum):
    LANDS: OtodomScraper = OtodomLandScraper
    HOUSES: OtodomScraper = OtodomHouseScraper
    APARTMENTS: OtodomScraper = OtodomApartmentScraper


class DomiportaScrapers(Enum):
    LANDS: DomiportaScraper = DomiportaLandScraper
    HOUSES: DomiportaScraper = DomiportaHouseScraper
    APARTMENTS: DomiportaScraper = DomiportaApartmentScraper


# Job types Enum
class JobTypes(Enum):
    SEARCH: str = "SEARCH"
    SCRAPE: str = "SCRAPE"
