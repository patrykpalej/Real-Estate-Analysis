import pickle
import unittest
from unittest.mock import patch
from datetime import datetime
from bs4 import BeautifulSoup

from exceptions import InvalidOffer
from scraping.otodom.otodom_lot_scraper import OtodomLotScraper


class TestOtodomLotScraper(unittest.TestCase):
    def test_init(self):
        scraper = OtodomLotScraper("test")

        self.assertEqual(scraper.name, "test")
        self.assertEqual(scraper.PROPERTY_TYPE, "LOTS")
        self.assertEqual(scraper.SUB_URL, "pl/oferty/sprzedaz/dzialka/cala-polska")

    def test_parse_offer_soup(self):
        scraper = OtodomLotScraper("test")

        with open("mock_data/otodom/offer_soup_lot_1.pickle", "rb") as f:
            test_soup = pickle.load(f)

        test_offer_model = scraper._parse_offer_soup(test_soup)

        self.assertEqual(test_offer_model.number_id, 64329729)
        self.assertEqual(test_offer_model.short_id, "4lW6h")
        self.assertEqual(test_offer_model.long_id,
                         "dzialka-4-750-m-skarzysko-kamienna-ID4lW6h")
        self.assertEqual(test_offer_model.url,
                         "https://www.otodom.pl/pl/oferta/dzialka-4-750-m-skarzysko-kamienna-ID4lW6h")
        self.assertEqual(test_offer_model.title,
                         "Działka, 4 750 m², Skarżysko-Kamienna")
        self.assertEqual(test_offer_model.price, 712000)
        self.assertEqual(test_offer_model.advertiser_type, "business")
        self.assertEqual(test_offer_model.advert_type, "AGENCY")
        self.assertEqual(test_offer_model.utc_created_at,
                         datetime(2023, 6, 16, 17, 21, 15))
        self.assertIsInstance(test_offer_model.utc_scraped_at, datetime)
        self.assertIsInstance(test_offer_model.description, str)
        self.assertEqual(test_offer_model.city, "Skarżysko-Kamienna")
        self.assertEqual(test_offer_model.subregion, "powiat-skarzyski")
        self.assertEqual(test_offer_model.province, "swietokrzyskie")
        self.assertEqual(test_offer_model.location, None)
        self.assertEqual(test_offer_model.latitude, 51.1144)
        self.assertEqual(test_offer_model.longitude, 20.8657)
        self.assertEqual(test_offer_model.lot_area, 4750)
        self.assertEqual(test_offer_model.lot_features,
                         '{"Media": ["prąd", "kanalizacja", "woda"], "Dojazd": ["asfaltowy"]}')
        self.assertEqual(test_offer_model.vicinity, None)

    @patch('scraping.abstract.otodom_scraper.OtodomScraper._get_raw_offer_data_from_offer_soup')
    def test_invalid_offers(self, raw_offer_mock):
        invalid_offer_1 = {"target": {
            "Country": "Niemcy",
            "OfferType": "sprzedaz"
        }}

        invalid_offer_2 = {"target": {
            "Country": "Polska",
            "OfferType": "kupno"
        }}

        raw_offer_mock.return_value = invalid_offer_1
        scraper = OtodomLotScraper("test1")
        with self.assertRaises(InvalidOffer):
            scraper._parse_offer_soup(BeautifulSoup())

        raw_offer_mock.return_value = invalid_offer_2
        scraper = OtodomLotScraper("test2")
        with self.assertRaises(InvalidOffer):
            scraper._parse_offer_soup(BeautifulSoup())
