import unittest

from utils.general import random_sleep


class TestFunctions(unittest.TestCase):
    def test_random_sleep(self):
        self.assertEqual(random_sleep(0), None)
