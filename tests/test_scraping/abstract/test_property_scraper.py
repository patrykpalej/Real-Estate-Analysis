import requests
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from bs4 import BeautifulSoup

from scraping.otodom.otodom_lot_scraper import OtodomLotScraper


class TestPopertyScraper(unittest.TestCase):
    """
    This class tests functionalities which are implemented in PropertyScraper
    It instantiates OtodomLotScraper becase PropertyScraper is abstract
    """
    def test_init(self):
        scraper = OtodomLotScraper("test")

        self.assertEqual(scraper.name, "test")
        self.assertIsInstance(scraper.created_at, datetime)

    def test_repr(self):
        scraper = OtodomLotScraper("test")
        self.assertEqual(scraper.__repr__(), f"Scraper: {scraper.name}")

    def test_str(self):
        scraper = OtodomLotScraper("test")
        self.assertEqual(scraper.__str__(), f"Scraper: {scraper.name}")

    def test_generate_headers(self):
        headers = OtodomLotScraper("test")._generate_headers()
        self.assertIsInstance(headers, dict)

        for key, value in headers.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, str)

    @patch('requests.get')
    def test_request_http_get(self, mock_requests_get):
        mock_response = MagicMock(spec=requests.Response,
                                  status_code=200, text="<html></html>")
        mock_requests_get.return_value = mock_response

        response = OtodomLotScraper("test")._request_http_get("a")
        self.assertIsInstance(response, requests.Response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "<html></html>")

    def test_make_soup(self):
        response_text = "<html><body><h1>Hello, World!</h1></body></html>"
        response = requests.Response()
        response._content = response_text.encode('utf-8')
        expected_output = BeautifulSoup(response_text, "html.parser")

        scraper = OtodomLotScraper("test")
        actual_output = scraper._make_soup(response)

        self.assertEqual(actual_output, expected_output)
