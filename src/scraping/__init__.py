from enum import Enum


class Services(Enum):
    OTODOM: str = "OTODOM"
    DOMIPORTA: str = "DOMIPORTA"


class PropertyTypes(Enum):
    LOTS: str = "LOTS"
    HOUSES: str = "HOUSES"
    APARTMENTS: str = "APARTMENTS"
