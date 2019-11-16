import unittest
import json

from QueryEngine.query_parser import extract_ontology_field, extract_ontology_keys


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
