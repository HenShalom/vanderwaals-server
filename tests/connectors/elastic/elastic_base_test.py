import unittest
from Connector.Elastic.ElasticBaseConnector import ElasticBaseConnector
from Queries.BasicQuery import BasicQuery
from Queries.QueryItem import QueryItem
from tests.connectors.elastic.elastic_common import elastic_template_query, empty_schema


class TestElasticBaseConnector(unittest.TestCase):
    def test__generate_query_item__query_item(self):
        elastic_index_connector = ElasticBaseConnector(empty_schema)
        item = QueryItem("test", "value")
        generate_query = elastic_index_connector.generate_query_item(item)
        self.assertEqual(generate_query, "(test=value)")

    def test__generate_query_item__basic_query(self):
        elastic_index_connector = ElasticBaseConnector(empty_schema)
        item = QueryItem("test", "value")
        basic_query = BasicQuery([item])
        generate_query = elastic_index_connector.generate_query_item(basic_query)
        self.assertEqual(generate_query, "(test=value)")

    def test__generate_basic_query__one_query(self):
        elastic_index_connector = ElasticBaseConnector(empty_schema)
        item = [QueryItem("test", "value")]
        basic_query = BasicQuery(item, operator="AND")
        generate_query = elastic_index_connector.generate_basic_query(basic_query)
        result = elastic_template_query
        result["query"]["query_string"]["query"] = "(test=value)"
        self.assertDictEqual(generate_query, result)

    def test__generate_basic_query__with_fields(self):
        elastic_index_connector = ElasticBaseConnector(empty_schema)
        item = [QueryItem("test", "value")]
        return_list = ["test1", "test2"]
        basic_query = BasicQuery(item, return_list=return_list, operator="AND")
        generate_query = elastic_index_connector.generate_basic_query(basic_query)
        result = elastic_template_query
        result["query"]["query_string"]["query"] = "(test=value)"
        result["_source"] = return_list
        self.assertDictEqual(generate_query, result)

    def test__generate_basic_query__multi_query(self):
        elastic_index_connector = ElasticBaseConnector(empty_schema)
        item = [QueryItem("test", "value"), QueryItem("test_two", "test_two")]
        basic_query = BasicQuery(item, operator="AND")
        generate_query = elastic_index_connector.generate_basic_query(basic_query)
        result = elastic_template_query
        result["query"]["query_string"]["query"] = "((test=value) AND (test_two=test_two))"
        self.assertDictEqual(generate_query, result)
