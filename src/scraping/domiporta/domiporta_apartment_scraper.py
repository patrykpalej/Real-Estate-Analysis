import re
import unicodedata
from bs4 import BeautifulSoup
from datetime import datetime, timezone

from scraping.abstract.domiporta_scraper import DomiportaScraper
from data.models.domiporta import DomiportaApartmentOffer
from scraping import PropertyTypes
from exceptions import InvalidOffer


class DomiportaApartmentScraper(DomiportaScraper):
    PROPERTY_TYPE: str = PropertyTypes.APARTMENTS.value
    SUB_URL: str = "mieszkanie/sprzedam"

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
                target_data["area"] = float(
                    re.sub(r"\s", "", value).replace(",", ".")
                    .replace("m2", "").strip())

            if name == "Rok budowy":
                target_data["build_year"] = int(value)

            if name == "Liczba pokoi":
                target_data["n_rooms"] = int(value)

        return target_data

    def _parse_offer_soup(
            self, offer_soup: BeautifulSoup) -> DomiportaApartmentOffer | None:
        """
        Creates DomiportaApartmentOffer instance (data model) from an offer soup

        Args:
            offer_soup (BeautifulSoup): single offer soup

        Returns:
            (DomiportaApartmentOffer): single offer data model

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
        title = re.sub(r"\s+", " ", offer_soup.find("h1")
                       .find_all("span")[0].text.strip())
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
        area = target_data["area"]
        build_year = target_data["build_year"]
        n_rooms = target_data["n_rooms"]

        offer_model = DomiportaApartmentOffer(
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
            area=area,
            build_year=build_year,
            n_rooms=n_rooms
        )

        offer_model.put_none_to_empty_values()
        return offer_model
