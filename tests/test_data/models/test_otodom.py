import unittest
from datetime import datetime

from data.models.otodom import OtodomOffer, OtodomLotOffer, OtodomHouseOffer, OtodomApartmentOffer


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


class TestOtodomLotOffer(unittest.TestCase):
    def test_attributes(self):
        otodom_lot_offer = OtodomLotOffer(
            number_id=123456,
            lot_area=120,
            lot_features="feat1|feat2|feat3",
            vicinity="{'a': ['abc', 'cde'], 'b': []}"
        )

        self.assertEqual(otodom_lot_offer.number_id, 123456)
        self.assertEqual(otodom_lot_offer.lot_area, 120)
        self.assertEqual(otodom_lot_offer.lot_features, "feat1|feat2|feat3")
        self.assertEqual(otodom_lot_offer.vicinity, "{'a': ['abc', 'cde'], 'b': []}")


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
