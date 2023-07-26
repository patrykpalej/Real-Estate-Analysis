import redis
import unittest

from data.storage.manager import StorageManager
from data.models.otodom import OtodomLotOffer


otodom_lot_offers = [
    OtodomLotOffer(number_id=123, short_id="abc", long_id="abcxyz", price=1234,
                   url="https://otodom.pl/abc", title="offer title"),
    OtodomLotOffer(number_id=234, short_id="def", long_id="defzyx", price=2345,
                   url="https://otodom.pl/def", title="offer title")
]


class TestStorageManager(unittest.TestCase):
    manager = StorageManager(service_name="otodom", property_type="lots",
                             scraper_name="ABC_XYZ", mode=0)

    def test_init(self):
        self.assertEqual(self.manager.service_name, "OTODOM")
        self.assertEqual(self.manager.property_type, "LOTS")
        self.assertEqual(self.manager.mode, 0)
        self.assertIsInstance(self.manager.redis_db, redis.Redis)

    def test_store_in_postgresql(self):
        self.manager.truncate_postgresql_table()

        self.manager.store_in_postgresql(otodom_lot_offers)
        data = self.manager.get_from_postgresql()

        self.assertEqual(list(data.iloc[0, :6].values),
                         [123, "abc", "abcxyz", "https://otodom.pl/abc",
                          "offer title", 1234])
        self.assertEqual(list(data.iloc[0, :6].index),
                         ["number_id", "short_id", "long_id", "url",
                          "title", "price"])
        self.assertEqual(len(data), 2)

        self.manager.truncate_postgresql_table()

    def test_store_in_mongodb(self):
        self.manager.truncate_mongodb_collection()

        self.manager.store_in_mongodb(otodom_lot_offers)
        data = list(self.manager.get_from_mongodb())

        self.assertEqual(data[0]["number_id"], 123)
        self.assertEqual(data[0]["short_id"], "abc")
        self.assertEqual(data[0]["long_id"], "abcxyz")
        self.assertEqual(data[0]["price"], 1234)
        self.assertEqual(data[0]["url"], "https://otodom.pl/abc")
        self.assertEqual(data[0]["title"], "offer title")

        self.assertEqual(data[1]["number_id"], 234)
        self.assertEqual(data[1]["short_id"], "def")
        self.assertEqual(data[1]["long_id"], "defzyx")
        self.assertEqual(data[1]["price"], 2345)
        self.assertEqual(data[1]["url"], "https://otodom.pl/def")
        self.assertEqual(data[1]["title"], "offer title")

        self.manager.truncate_mongodb_collection()

    def test_cache_data(self):
        self.assertIsNone(self.manager.read_cache("test"))

        self.manager.cache_data("test", ["url1", "url2", "url3"])
        self.assertEqual(self.manager.read_cache("test", from_json=True),
                         ["url1", "url2", "url3"])

        self.manager.clear_cache("test")
        self.assertIsNone(self.manager.read_cache("test"))
