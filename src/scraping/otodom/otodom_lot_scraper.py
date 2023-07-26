import json
import unicodedata
from bs4 import BeautifulSoup
from datetime import datetime, timezone

from scraping.abstract.otodom_scraper import OtodomScraper
from data.models.otodom import OtodomLotOffer
from scraping import PropertyTypes
from exceptions import InvalidOffer
from utils.general import smart_join


class OtodomLotScraper(OtodomScraper):
    PROPERTY_TYPE: str = PropertyTypes.LOTS.value
    SUB_URL: str = "pl/oferty/sprzedaz/dzialka/cala-polska"

    def __init__(self, scraper_name: str):
        super().__init__(scraper_name)

    def _parse_offer_soup(
            self, offer_soup: BeautifulSoup) -> OtodomLotOffer | None:
        """
        Creates OtodomLotOffer instance (data model) from an offer soup

        Args:
            offer_soup (BeautifulSoup): single offer soup

        Returns:
            (OtodomLotOffer): single offer data model

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
        lot_area = int(float(offer_json["target"]["Area"]))
        lot_features = json.dumps(
            {category["label"]: category["values"] for category in
             offer_json.get("featuresByCategory")}, ensure_ascii=False)
        vicinity = smart_join(offer_json["target"].get("Vicinity_types"))

        offer_model = OtodomLotOffer(
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
            lot_area=lot_area,
            lot_features=lot_features,
            vicinity=vicinity
        )

        offer_model.put_none_to_empty_values()
        return offer_model
