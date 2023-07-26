from enum import Enum


class Services(Enum):
    OTODOM: str = "OTODOM"
    DOMIPORTA: str = "DOMIPORTA"


class PropertyTypes(Enum):
    LOTS: str = "LOTS"
    HOUSES: str = "HOUSES"
    APARTMENTS: str = "APARTMENTS"


class ScrapingModes(Enum):
    TEST: int = 0
    DEV: int = 1
    PROD: int = 2
