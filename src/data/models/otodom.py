from dataclasses import dataclass
from datetime import datetime

from data.models.common import Offer


@dataclass
class OtodomOffer(Offer):
    number_id: int = None
    short_id: str = None
    long_id: str = None
    url: str = None
    title: str = None
    price: int = None
    advertiser_type: str = None
    advert_type: str = None
    utc_created_at: datetime = None
    utc_scraped_at: datetime = None
    description: str = None
    city: str = None
    subregion: str = None
    province: str = None
    location: str = None
    latitude: float = None
    longitude: float = None


@dataclass
class OtodomLotOffer(OtodomOffer):
    lot_area: int = None
    lot_features: str = None
    vicinity: str = None


@dataclass
class OtodomHouseOffer(OtodomOffer):
    market: str = None
    building_type: str = None
    house_features: str = None
    lot_area: int = None
    house_area: int = None
    n_rooms: int = None
    floors_info: str = None
    heating: str = None
    build_year: int = None
    media: str = None
    vicinity: str = None


@dataclass
class OtodomApartmentOffer(OtodomOffer):
    market: str = None
    status: list[str] = None
    apartment_features: str = None
    apartment_area: int = None
    build_year: int = None
    building_floors_num: int = None
    building_type: str = None
    elevator: bool = None
    media: str = None
    heating: str = None
    rent: int = None
    n_rooms: int = None
