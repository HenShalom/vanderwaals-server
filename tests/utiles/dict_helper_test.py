import unittest

from Utiles.dict_helpers import get_from_dict


class TestDictHelpers(unittest.TestCase):
    def test__get_from_dict(self):
        obj = {
            "test": {
                "test": {
                    "elastic": {
                        "value": 2
                    }
                }
            }
        }
        array_path = ["test", "test", "elastic", "value"]
        self.assertEqual(get_from_dict(obj, array_path), 2)
