import unittest

from QueryEngine.tagging_parser import *
from QueryEngine.TaggingGroup import TaggingGroup

tagging_items = [
    {
        "schema": "test",
        "collection": "test_collection",
        "table": "test_table",
        "bdt": "ID",
        "field": "id"
    },
    {
        "schema": "test",
        "collection": "test_collection",
        "table": "test_table",
        "bdt": "FullName",
        "field": "name"
    }
]


class TestTaggingParser(unittest.TestCase):
    def test__get_tagging_settings(self):
        tagging_group_settings = get_tagging_settings(tagging_items[0], group_by=["schema", "table"])
        results = {
            "schema": "test",
            "table": "test_table"
        }
        self.assertDictEqual(tagging_group_settings, results)

    def test__add_initial_settings_to_groups(self):
        group = TaggingGroup(tagging_items)
        groups = add_initial_settings_to_groups([group], group_by=["schema", "table"])
        group_settings = {
            "schema": "test",
            "table": "test_table"
        }
        self.assertDictEqual(groups[0].settings, group_settings)

    def test__get_group_by_key(self):
        group_key = get_group_by_key(tagging_items[0], group_by=["schema", "table"])
        self.assertEqual(group_key, "test~test_table")

    def test__get_groups_keys(self):
        group = TaggingGroup(tagging_items)
        keys_set = get_groups_keys(group)
        self.assertSetEqual(keys_set, {"ID", "FullName"})

    def test__is_keys_in_group__should_return_false(self):
        group = TaggingGroup(tagging_items)
        keys = {
            "ID": False,
            "Stuff": False  # this key is not optional and not in the group
        }
        self.assertTrue(not is_keys_in_group(keys, group))

    def test__is_keys_in_group__should_return_true(self):
        group = TaggingGroup(tagging_items)
        keys = {
            "ID": False,
            "Stuff": True  # this key is not in the group but optional
        }
        self.assertTrue(is_keys_in_group(keys, group))

    def test__is_keys_in_group__all_true(self):
        group = TaggingGroup(tagging_items)
        keys = {
            "ID": False,
            "FullName": False
        }
        self.assertTrue(is_keys_in_group(keys, group))
