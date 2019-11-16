import json
import unittest

from QueryEngine.Parser.query_parser import *
from tests.query_engine.tagging_parser_test import basic_group


class TestQueryParse(unittest.TestCase):
    def test_extract_ontology_field__return_fields(self):
        with open("Docs/basicQueryExample.json") as query_json:
            basic_query = json.load(query_json)
            basic_query_fields = extract_ontology_field(basic_query)
            extracted_queries = [
                {
                    "key": "ID",
                    "value": "25"
                },
                {
                    "key": "FullName",
                    "value": "Test",
                    "optional": True
                },
                {
                    "key": "Age",
                    "value": "24",
                    "optional": True
                }
            ]
            self.assertListEqual(basic_query_fields, extracted_queries)

    def test_extract_ontology_keys__return_fields(self):
        with open("Docs/basicQueryExample.json") as query_json:
            basic_query = json.load(query_json)
            basic_query_keys = extract_ontology_keys(basic_query)
            extracted_queries = {
                "ID": False,
                "FullName": True,
                "Age": True
            }
            self.assertDictEqual(basic_query_keys, extracted_queries)

    def test__generate_query_item(self):
        query_item_dict = {
            "key": "ID",
            "value": "25"
        }
        res = generate_query_item(query_item_dict, basic_group)
        self.assertTrue(type(res) == QueryItem)
        self.assertTrue(res.key == "id")
        self.assertTrue(res.value == "25")

    def test__generate_basic_query(self):
        with open("Docs/basicQueryExample.json") as query_json:
            query_dict = json.load(query_json)
            basic_query = generate_basic_query(query_dict, basic_group)
            print(basic_query.query_items)
            self.assertTrue(type(basic_query) == BasicQuery)
            self.assertTrue(len(basic_query.query_items) == 2)
            self.assertTrue(type(basic_query.query_items[0]) == BasicQuery)
