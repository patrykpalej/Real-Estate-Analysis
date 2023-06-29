import redis
import unittest

from data.storage.manager import StorageManager


class TestStorageManager(unittest.TestCase):
    def test_init(self):
        manager = StorageManager("abc", "xyz", 0)

        self.assertEqual(manager.service_name, "ABC")
        self.assertEqual(manager.property_type, "XYZ")
        self.assertEqual(manager.mode, 0)
        self.assertIsInstance(manager.redis_db, redis.Redis)
