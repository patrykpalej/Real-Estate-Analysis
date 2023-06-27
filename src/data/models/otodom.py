from dataclasses import dataclass
from datetime import datetime

from data.models.common import Offer


@dataclass
class OtodomOffer(Offer):
    number_id: int
    short_id: str
    long_id: str
    url: str
    title: str
    price: int
    advertiser_type: str
    advert_type: str
    utc_created_at: datetime
    utc_scraped_at: datetime
    description: str
    city: str
    subregion: str
    province: str
    location: str
    latitude: float
    longitude: float


@dataclass
class OtodomLotOffer(OtodomOffer):
    lot_area: int
    lot_features: str
    vicinity: str


@dataclass
class OtodomHouseOffer(OtodomOffer):
    market: str
    building_type: str
    house_features: str
    lot_area: int
    house_area: int
    n_rooms: int
    floors_info: str
    heating: str
    build_year: int
    media: str
    vicinity: str


@dataclass
class OtodomApartmentOffer(OtodomOffer):
    market: str
    status: list[str]
    apartment_features: str
    apartment_area: int
    build_year: int
    building_floors_num: int
    building_type: str
    elevator: bool
    media: str
    heating: str
    rent: int
    n_rooms: int
