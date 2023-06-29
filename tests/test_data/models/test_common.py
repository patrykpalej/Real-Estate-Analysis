import unittest
import pandas as pd

from data.models.common import Offer


offer = Offer()
offer.attr1 = 123
offer.attr2 = "abc"
offer.attr3 = '{"a": 1, "b": [1, 2, 3]}'


class TestOffer(unittest.TestCase):
    def test_to_dict(self):
        dict_parse_json = offer.to_dict(parse_json=True)
        dict_not_parse_json = offer.to_dict()

        self.assertEqual(dict_parse_json,
                         {"attr1": 123,
                          "attr2": "abc",
                          "attr3": {"a": 1, "b": [1, 2, 3]}})

        self.assertEqual(dict_not_parse_json,
                         {"attr1": 123,
                          "attr2": "abc",
                          "attr3": '{"a": 1, "b": [1, 2, 3]}'})

    def test_to_dataframe(self):
        df = offer.to_dataframe()

        self.assertTrue(df.equals(pd.DataFrame(
                             {"attr1": [123],
                              "attr2": ["abc"],
                              "attr3": ['{"a": 1, "b": [1, 2, 3]}']}
                         )))

    def test_put_none_to_empty_values(self):
        offer = Offer()
        offer.attr1 = ""
        offer.attr2 = []
        offer.attr3 = 0
        offer.attr4 = "[]"

        offer.put_none_to_empty_values()

        self.assertEqual(offer.attr1, None)
        self.assertEqual(offer.attr2, None)
        self.assertEqual(offer.attr3, None)
        self.assertEqual(offer.attr4, None)
