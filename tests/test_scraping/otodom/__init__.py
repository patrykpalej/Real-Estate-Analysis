import unittest

from scraping.otodom import OtodomSearchParams, OtodomLandSearchParams


search_params = OtodomSearchParams()
keys = ["ownerTypeSingleSelect", "limit", "daysSinceCreated",
        "by", "direction", "viewType"]


class TestOtodomSearchParams(unittest.TestCase):
    def test_init(self):
        self.assertEqual(search_params.ownerTypeSingleSelect, "ALL")
        self.assertEqual(search_params.viewType, "listing")

    def test_set_param(self):
        self.assertFalse(hasattr(search_params, "my_param"))

        search_params.set_param("my_param", 1)
        self.assertTrue(hasattr(search_params, "my_param"))
        self.assertEqual(search_params.my_param, 1)

        del search_params.my_param

    def test_to_dict(self):
        search_params_dict = search_params.to_dict()
        self.assertIsInstance(search_params_dict, dict)

        for key in keys:
            self.assertIn(key, search_params_dict.keys())

        self.assertNotIn("priceMin", search_params_dict.keys())
        self.assertNotIn("priceMax", search_params_dict.keys())


class TestOtodomLandSearchParams(unittest.TestCase):
    def test_init(self):
        search_params = OtodomLandSearchParams()

        for key in keys:
            self.assertIn(key, search_params.__dict__.keys())

        self.assertEqual(search_params.areaMin, None)
        self.assertEqual(search_params.areaMax, None)
        self.assertEqual(search_params.plotType, "[BUILDING]")
        self.assertEqual(search_params.pricePerMeterMin, None)
        self.assertEqual(search_params.pricePerMeterMax, None)
