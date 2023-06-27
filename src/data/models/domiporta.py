from dataclasses import dataclass
from datetime import datetime

from data.models.common import Offer


@dataclass
class DomiportaOffer(Offer):
    pass


@dataclass
class DomiportaLotOffer(DomiportaOffer):
    pass


@dataclass
class DomiportaHouseOffer(DomiportaOffer):
    pass


@dataclass
class DomiportaApartmentOffer(DomiportaOffer):
    pass
