import unittest
from unittest import mock
from datetime import date
import requests
import requests_mock

from scraping.otodom.otodom_lot_scraper import OtodomLotScraper


scraper = OtodomLotScraper("my_scraper")


class GeneralTests(unittest.TestCase):
    def test_scraper_information(self):
        self.assertEqual(scraper.name, "my_scraper")
        self.assertEqual(scraper.service_name, "OTODOM")
        self.assertEqual(scraper.created_at.date(), date.today())

    def test_scraper_representation(self):
        pass


class HttpRequesting(unittest.TestCase):
    def test_request_http_get(self):
        response = scraper._request_http_get("https://example.com/")
        self.assertEqual(response.ok, True)
        self.assertEqual(response.status_code, 200)

    def test_mock(self):
        pass
        # session = requests.Session()
        # adapter = requests_mock.Adapter()
        # session.mount('mock://', adapter)
        #
        # adapter.register_uri('GET', 'mock://palej.tech', text='data123')
        # response = session.get('mock://palej.tech')
        # print(response.text)


if __name__ == '__main__':
    unittest.main()
