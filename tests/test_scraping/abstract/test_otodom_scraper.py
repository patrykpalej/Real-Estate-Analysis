import json
import pickle
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from data.models.otodom import OtodomOffer
from scraping.otodom.otodom_lot_scraper import OtodomLotScraper


class TestOtodomScraper(unittest.TestCase):
    """
    This class tests functionalities which are implemented in OtodomScraper
    It instantiates OtodomLotScraper becase OtodomScraper is abstract
    """
    scraper = OtodomLotScraper("test")

    def test_init(self):
        self.assertEqual(self.scraper.SERVICE_NAME, "OTODOM")
        self.assertEqual(self.scraper.BASE_URL, "https://www.otodom.pl/")
        self.assertEqual(self.scraper.OFFER_BASE_URL,
                         "https://www.otodom.pl/pl/oferta/")

    def test_get_raw_offer_data_from_offer_soup(self):
        soup_files = sorted(
            Path("mock_data/otodom")
            .glob("offer_soup*.pickle"))

        raw_data_files = sorted(
            Path("mock_data/otodom")
            .glob("offer_raw_data*.json"))

        for soup_file, raw_data_file in zip(soup_files, raw_data_files):
            with open(soup_file, "rb") as f:
                soup = pickle.load(f)

            with open(raw_data_file, "r") as f:
                expected_raw_data = json.load(f)

            actual_raw_data = \
                self.scraper._get_raw_offer_data_from_offer_soup(soup)

            self.assertIsInstance(actual_raw_data, dict)

            for expected, actual in zip(expected_raw_data, actual_raw_data):
                self.assertEqual(expected, actual)

    def test_get_offers_urls_from_single_search_page(self):
        soup_files = sorted(
            Path("mock_data/otodom")
            .glob("search_soup*.pickle"))

        urls_files = sorted(
            Path("mock_data/otodom")
            .glob("search_urls*.json"))

        for soup_file, urls_file in zip(soup_files, urls_files):
            with open(soup_file, "rb") as f:
                soup = pickle.load(f)

            with open(urls_file, "r") as f:
                expected_urls_list = json.load(f)

            actual_urls_list = \
                self.scraper._get_offers_urls_from_single_search_page(soup)

            self.assertIsInstance(actual_urls_list, list)
            self.assertEqual(expected_urls_list, actual_urls_list)
            self.assertNotEqual(actual_urls_list, [])

    def test_get_offers_urls_from_empty_search_page(self):
        soup_files = sorted(
            Path("mock_data/otodom")
            .glob("empty_search_soup*.pickle"))

        for soup_file in soup_files:
            with open(soup_file, "rb") as f:
                soup = pickle.load(f)

            actual_urls_list = \
                self.scraper._get_offers_urls_from_single_search_page(soup)

            self.assertEqual(actual_urls_list, [])

    def test_scrape_offer_from_url(self):
        scraper = OtodomLotScraper("test")
        url = "https://example.com/offer"
        headers = scraper._generate_headers()

        response_mock = MagicMock()
        soup_mock = MagicMock()
        data_model_mock = OtodomOffer()

        scraper._request_http_get = MagicMock(return_value=response_mock)
        scraper._make_soup = MagicMock(return_value=soup_mock)
        scraper._parse_offer_soup = MagicMock(return_value=data_model_mock)
        scraper._generate_headers = MagicMock(return_value=headers)

        result = scraper.scrape_offer_from_url(url)

        self.assertEqual(result, data_model_mock)
        scraper._request_http_get.assert_called_once_with(
            url, headers=headers)
        scraper._make_soup.assert_called_once_with(response_mock)
        scraper._parse_offer_soup.assert_called_once_with(soup_mock)

    def test_list_offers_urls_from_search_params(self):
        scraper = OtodomLotScraper("test")
        search_params = {"param1": "value1", "param2": "value2"}
        n_pages = 2
        avg_sleep_time = 0

        response_mock = MagicMock()
        soup_mock = MagicMock()
        headers_mock = MagicMock()
        single_page_urls_mock = ["url1", "url2", "url3"]
        all_urls_mock = (single_page_urls_mock * n_pages,
                         [len(single_page_urls_mock)] * n_pages)

        scraper._request_http_get = MagicMock(return_value=response_mock)
        scraper._make_soup = MagicMock(return_value=soup_mock)
        scraper._get_offers_urls_from_single_search_page = MagicMock(
            return_value=single_page_urls_mock)
        scraper._generate_headers = MagicMock(return_value=headers_mock)

        result = scraper.list_offers_urls_from_search_params(
            search_params, n_pages, avg_sleep_time)

        self.assertEqual(result, all_urls_mock)
        self.assertEqual(scraper._request_http_get.call_count, n_pages)
        self.assertEqual(scraper._make_soup.call_count, n_pages)
