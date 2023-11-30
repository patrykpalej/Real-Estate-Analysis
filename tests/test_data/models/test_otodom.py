import unittest
from datetime import datetime

from data.models.otodom import OtodomOffer, OtodomLandOffer, OtodomHouseOffer, OtodomApartmentOffer


class TestOtodomOffer(unittest.TestCase):
    def test_attributes(self):
        otodom_offer = OtodomOffer(
            number_id=123456,
            short_id="xyz",
            long_id="123xyz456",
            utc_created_at=datetime(2000, 1, 14),
            utc_scraped_at=datetime.now(),
            latitude=50.123456,
            longitude=20.987654,
        )

        self.assertEqual(otodom_offer.number_id, 123456)
        self.assertEqual(otodom_offer.short_id, "xyz")
        self.assertEqual(otodom_offer.long_id, "123xyz456")
        self.assertEqual(otodom_offer.utc_created_at, datetime(2000, 1, 14))
        self.assertIsInstance(otodom_offer.utc_scraped_at, datetime)
        self.assertEqual(otodom_offer.latitude, 50.123456)
        self.assertEqual(otodom_offer.longitude, 20.987654)
        self.assertEqual(otodom_offer.url, None)


class TestOtodomLandOffer(unittest.TestCase):
    def test_attributes(self):
        otodom_land_offer = OtodomLandOffer(
            number_id=123456,
            land_area=120,
            land_features="feat1|feat2|feat3",
            vicinity="{'a': ['abc', 'cde'], 'b': []}"
        )

        self.assertEqual(otodom_land_offer.number_id, 123456)
        self.assertEqual(otodom_land_offer.land_area, 120)
        self.assertEqual(otodom_land_offer.land_features, "feat1|feat2|feat3")
        self.assertEqual(otodom_land_offer.vicinity, "{'a': ['abc', 'cde'], 'b': []}")


class TestOtodomHouseOffer(unittest.TestCase):
    def test_attributes(self):
        otodom_house_offer = OtodomHouseOffer(
            number_id=123456,
            market="abc",
            building_type="xyz",
            house_features="{'a': ['abc', 'cde'], 'b': []}"
        )

        self.assertEqual(otodom_house_offer.number_id, 123456)
        self.assertEqual(otodom_house_offer.market, "abc")
        self.assertEqual(otodom_house_offer.building_type, "xyz")
        self.assertEqual(otodom_house_offer.house_features, "{'a': ['abc', 'cde'], 'b': []}")


class TestOtodomApartmentOffer(unittest.TestCase):
    def test_attributes(self):
        otodom_apartment_offer = OtodomApartmentOffer(
            number_id=123456,
            market="abc",
            status=["a", "b", "c"],
            apartment_features="{'a': ['abc', 'cde'], 'b': []}"
        )

        self.assertEqual(otodom_apartment_offer.number_id, 123456)
        self.assertEqual(otodom_apartment_offer.market, "abc")
        self.assertEqual(otodom_apartment_offer.status, ["a", "b", "c"])
        self.assertEqual(otodom_apartment_offer.apartment_features, "{'a': ['abc', 'cde'], 'b': []}")
