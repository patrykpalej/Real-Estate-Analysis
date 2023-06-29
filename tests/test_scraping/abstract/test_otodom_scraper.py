import unittest

from scraping.otodom.otodom_lot_scraper import OtodomLotScraper


class TestOtodomScraper(unittest.TestCase):
    """
    This class tests functionalities which are implemented in OtodomScraper
    It instantiates OtodomLotScraper becase OtodomScraper is abstract
    """
    def test_init(self):
        scraper = OtodomLotScraper("abc")

        self.assertEqual(scraper.SERVICE_NAME, "OTODOM")
        self.assertEqual(scraper.BASE_URL, "https://www.otodom.pl/")
        self.assertEqual(scraper.OFFER_BASE_URL, "https://www.otodom.pl/pl/oferta/")

    def test_get_raw_offer_data_from_offer_soup(self):
        pass

    def test_get_offers_urls_from_single_search_page(self):
        pass

    def test_list_offers_urls_from_search_params(self):
        pass

    def test_scrape_offer_from_url(self):
        pass
