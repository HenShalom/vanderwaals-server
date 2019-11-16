import unittest
from Connector.Elastic.ElasticSingleIndexConnector import ElasticSingleIndexConnector
from Queries.AdvanceQuery import AdvanceQuery
from Queries.BasicQuery import BasicQuery
from Queries.QueryItem import QueryItem
from tests.connectors.elastic.elastic_common import *


class TestElasticMultiIndexConnector(unittest.TestCase):
    def test__get_query_body__one_query(self):
        elastic_index_connector = ElasticSingleIndexConnector(schema_with_table)
        return_list = ["test1", "test2"]
        item = [QueryItem("test", "value"), QueryItem("test_two", "test_two")]
        basic_query = BasicQuery(item, return_list=return_list, operator="AND", table_name="test")
        advance_query = AdvanceQuery(basic_query)
        generate_query = elastic_index_connector.get_query_body(advance_query)
        data_query = elastic_template_query
        data_query["query"]["query_string"]["query"] = "((_table=test) AND (test=value) AND (test_two=test_two))"
        data_query["_source"] = return_list
        location = {
            "index": "main_index",
        }
        self.assertListEqual(generate_query, [location, data_query])

    def test__generate_location_query_item__only_table(self):
        elastic_index_connector = ElasticSingleIndexConnector(schema_with_table)
        basic_query = BasicQuery([], table_name="test")
        location_basic_query = elastic_index_connector.generate_location_query_item(basic_query)
        location_string_query = elastic_index_connector.generate_query_item(location_basic_query)
        table_query_item = QueryItem("_table", "test")
        result_string_query = elastic_index_connector.generate_query_item(BasicQuery([table_query_item]))
        self.assertEqual(location_string_query, result_string_query)

    def test__generate_location_query_item__table_and_collection(self):
        elastic_index_connector = ElasticSingleIndexConnector(schema_with_collection)
        basic_query = BasicQuery([], table_name="test", collection_name="collection_test")
        location_basic_query = elastic_index_connector.generate_location_query_item(basic_query)
        location_string_query = elastic_index_connector.generate_query_item(location_basic_query)
        table_query_item = QueryItem("_table", "test")
        collection_query_item = QueryItem("_collection", "collection_test")
        result_string_query = elastic_index_connector.generate_query_item(
            BasicQuery([table_query_item, collection_query_item]))
        self.assertEqual(location_string_query, result_string_query)

    def test__generate_basic_query_location__location(self):
        schema = {
            **empty_schema,
            "type": "main_type"
        }
        elastic_index_connector = ElasticSingleIndexConnector(schema)
        location_query = elastic_index_connector.generate_basic_query_location()
        self.assertDictEqual(location_query, {
            "index": "main_index",
            "type": "main_type"
        })

    def test__generate_basic_query_location__basic_location(self):
        elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
        location_query = elastic_index_connector.generate_basic_query_location()
        self.assertDictEqual(location_query, {
            "index": "main_index",
        })
