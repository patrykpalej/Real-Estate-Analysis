import unittest
from datetime import date

from utils.scraping import generate_random_headers, generate_scraper_name


class TestFunctions(unittest.TestCase):
    def test_generate_random_headers(self):
        headers = generate_random_headers()

        self.assertIsInstance(headers, dict)
        for key, value in headers.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, str)

    def test_generate_scraper_name(self):
        # str.upper()
        self.assertRegex(generate_scraper_name("abc", "xyz", "ijk"),
                         r"^\d*-\d*_ABC_XYZ_IJK$")

        # date.today()
        self.assertRegex(generate_scraper_name("ABC", "XYZ", "IJK"),
                         rf"^{date.today().strftime('%Y%m%d')}-\d*_ABC_XYZ_IJK$")
