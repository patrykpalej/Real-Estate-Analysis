from dataclasses import dataclass
from datetime import datetime

from data.models.common import Offer


@dataclass
class DomiportaOffer(Offer):
    number_id: str = None
    url: str = None
    title: str = None
    price: int = None
    utc_scraped_at: datetime = None
    description: str = None
    city: str = None
    province: str = None
    latitude: float = None
    longitude: float = None


@dataclass
class DomiportaLotOffer(DomiportaOffer):
    lot_area: int = None
    driveway: str = None
    media: str = None


@dataclass
class DomiportaHouseOffer(DomiportaOffer):
    lot_area: int = None
    driveway: str = None
    media: str = None
    area: float = None
    build_year: int = None
    n_rooms: int = None
    building_type: str = None


@dataclass
class DomiportaApartmentOffer(DomiportaOffer):
    area: float = None
    build_year: int = None
    n_rooms: int = None
