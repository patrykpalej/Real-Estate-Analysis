import re
import unicodedata
from bs4 import BeautifulSoup
from datetime import datetime, timezone

from scraping.abstract.domiporta_scraper import DomiportaScraper
from data.models.domiporta import DomiportaLotOffer
from scraping import PropertyTypes
from exceptions import InvalidOffer


class DomiportaLotScraper(DomiportaScraper):
    PROPERTY_TYPE: str = PropertyTypes.LOTS.value
    SUB_URL: str = "dzialki-budowlane/sprzedam"

    def __init__(self, scraper_name: str):
        super().__init__(scraper_name)

    @staticmethod
    def _get_target_data_from_offer_soup(offer_soup: BeautifulSoup) -> dict:
        target_data = {}

        for item in offer_soup.find("ul", "features__list-2").find_all("li"):
            name = item.find("span", "features__item_name").text.strip()
            value = item.find("span", "features__item_value").text.strip()

            if name == "Cena":
                target_data["price"] = int(re.sub(r"\D", "", value))

            if name == "Powierzchnia całkowita":
                target_data["lot_area"] = int(
                    re.sub(r"\s", "", value).replace("m2", "").strip())

            if name == "Droga dojazdowa":
                target_data["driveway"] = value

            if name == "Media":
                target_data["media"] = value

        return target_data

    def _parse_offer_soup(
            self, offer_soup: BeautifulSoup) -> DomiportaLotOffer | None:
        """
        Creates DomiportaLotOffer instance (data model) from an offer soup

        Args:
            offer_soup (BeautifulSoup): single offer soup

        Returns:
            (DomiportaLotOffer): single offer data model

        """
        country = offer_soup.find_all(
            "meta", {"itemprop": "addressCountry"})[0]["content"]
        if country != "Polska":
            raise InvalidOffer("Offer from another country")

        target_data = self._get_target_data_from_offer_soup(offer_soup)

        coordinates_dict = {}
        for item in offer_soup.find("span", {"itemprop": "geo"}).find_all("meta"):
            coordinates_dict[item["itemprop"]] = float(
                item["content"].replace(",", "."))

        number_id = (offer_soup.find("div", "detials_bar_data")
                               .find("input", {"type": "hidden"})["value"])
        url = offer_soup.find("link", {"rel": "canonical"})["href"]
        title = offer_soup.find("h1").find_all("span")[0].text.strip()
        price = target_data["price"]
        utc_scraped_at = datetime.now(tz=timezone.utc)
        description = unicodedata.normalize("NFKC", offer_soup.find(
            "div", "description__panel").text.strip())
        city = offer_soup.find_all(
            "span", {"itemprop": "addressLocality"})[0].text
        province = offer_soup.find_all(
            "meta", {"itemprop": "addressRegion"})[0]["content"]
        longitude = coordinates_dict["longitude"]
        latitude = coordinates_dict["latitude"]
        lot_area = target_data["lot_area"]
        driveway = target_data.get("driveway")
        media = target_data.get("media")

        offer_model = DomiportaLotOffer(
            number_id=number_id,
            url=url,
            title=title,
            price=price,
            utc_scraped_at=utc_scraped_at,
            description=description,
            city=city,
            province=province,
            longitude=longitude,
            latitude=latitude,
            lot_area=lot_area,
            driveway=driveway,
            media=media
        )

        offer_model.put_none_to_empty_values()
        return offer_model
