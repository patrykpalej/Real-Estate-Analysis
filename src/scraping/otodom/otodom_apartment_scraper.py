import unicodedata
from bs4 import BeautifulSoup
from datetime import datetime, timezone

from scraping.abstract.otodom_scraper import OtodomScraper
from data.models.otodom import OtodomApartmentOffer
from scraping import PropertyTypes
from exceptions import InvalidOffer
from utils.general import smart_join, smart_cast, smart_slice


class OtodomApartmentScraper(OtodomScraper):
    PROPERTY_TYPE: str = PropertyTypes.HOUSES.value
    SUB_URL: str = "pl/oferty/sprzedaz/mieszkanie/cala-polska"

    def __init__(self, scraper_name: str):
        super().__init__(scraper_name)

    @staticmethod
    def _convert_floor_num(floor_txt: str):
        """
        Converts text description of floor number to int
        """
        try:
            return int(floor_txt.split("_")[-1])
        except Exception as e:
            return None

    def _parse_offer_soup(
            self, offer_soup: BeautifulSoup) -> OtodomApartmentOffer | None:
        """
        Creates OtodomApartmentOffer instance (data model) from an offer soup

        Args:
            offer_soup (BeautifulSoup): single offer soup

        Returns:
            (OtodomApartmentOffer): single offer data model

        """
        try:
            offer_json = self._get_raw_offer_data_from_offer_soup(offer_soup)
        except Exception as e:
            self._log.error(e)
            raise InvalidOffer("Soup does not contain valid offer json")

        if offer_json["target"].get("Country") != "Polska":
            raise InvalidOffer("Offer from another country")

        if offer_json["target"].get("OfferType") != "sprzedaz":
            raise InvalidOffer("Not a sales offer")

        number_id = offer_json["id"]
        short_id = offer_json["publicId"]
        long_id = offer_json["slug"]
        url = offer_json["url"]
        title = offer_json["title"]
        price = int(offer_json["target"]["Price"])
        advertiser_type = offer_json["advertiserType"]
        advert_type = offer_json["advertType"]
        utc_created_at = datetime.fromisoformat(
            offer_json["createdAt"]).replace(tzinfo=None)
        utc_scraped_at = datetime.now(tz=timezone.utc)
        description = unicodedata.normalize("NFKC", BeautifulSoup(
            offer_json["description"], "html.parser").text)
        city = offer_json["location"]["address"]["city"]["name"]
        subregion = offer_json["location"]["address"]["county"]["code"]
        province = offer_json["location"]["address"]["province"]["code"]
        location = smart_join(offer_json["target"].get("Location"))
        longitude = offer_json["location"]["coordinates"]["longitude"]
        latitude = offer_json["location"]["coordinates"]["latitude"]
        market = offer_json.get("market")
        status = smart_join(offer_json["target"].get("Construction_status"))
        apartment_features = smart_join(offer_json["features"])
        apartment_area = int(float(offer_json["target"]["Area"]))
        build_year = smart_cast(offer_json["target"].get("Build_year"), int)
        floor = self._convert_floor_num(offer_json["target"].get("Floor_no"))
        building_floors_num = smart_cast(
            offer_json["target"].get("Building_floors_num"), int)
        building_type = smart_join(offer_json["target"].get("Building_type"))
        media = smart_join(offer_json["target"].get("Media_types"))
        heating = smart_join(offer_json["target"].get("Heating_types"))
        n_rooms = smart_cast(
            smart_slice(offer_json["target"].get("Rooms_num")), int)

        offer_model = OtodomApartmentOffer(
            number_id=number_id,
            short_id=short_id,
            long_id=long_id,
            url=url,
            title=title,
            price=price,
            advertiser_type=advertiser_type,
            advert_type=advert_type,
            utc_created_at=utc_created_at,
            utc_scraped_at=utc_scraped_at,
            description=description,
            city=city,
            subregion=subregion,
            province=province,
            location=location,
            longitude=longitude,
            latitude=latitude,
            market=market,
            status=status,
            apartment_features=apartment_features,
            apartment_area=apartment_area,
            build_year=build_year,
            floor=floor,
            building_floors_num=building_floors_num,
            building_type=building_type,
            media=media,
            heating=heating,
            n_rooms=n_rooms,
        )

        offer_model.put_none_to_empty_values()
        return offer_model
