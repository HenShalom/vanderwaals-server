import unittest
from Connector.ElasticSingleIndexConnector.ElasticSingleIndexConnector import ElasticSingleIndexConnector
from Queries.QueryItem import QueryItem
from Queries.BasicQuery import BasicQuery
from Queries.AdvanceQuery import AdvanceQuery

empty_schema = {
    "connection": {
        "hosts": ["localhost:9200"],
    }
}

elastic_template_query = {
    "query": {
        "query_string": {
            "query": ""
        }
    }
}


class TestElasticSingleIndex(unittest.TestCase):
    def test__generate_query_item__query_item(self):
        elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
        item = QueryItem("test", "value")
        generate_query = elastic_index_connector.generate_query_item(item)
        self.assertEquals(generate_query, "(test=value)")

    def test__generate_query_item__basic_query(self):
        elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
        item = QueryItem("test", "value")
        basic_query = BasicQuery([item])
        generate_query = elastic_index_connector.generate_query_item(basic_query)
        self.assertEquals(generate_query, "(test=value)")

    def test__generate_basic_query__one_query(self):
        elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
        item = [QueryItem("test", "value")]
        basic_query = BasicQuery(item, operator="AND")
        generate_query = elastic_index_connector.generate_basic_query(basic_query)
        result = elastic_template_query
        result["query"]["query_string"]["query"] = "(test=value)"
        self.assertDictEqual(generate_query, result)

    def test__generate_basic_query__with_fields(self):
        elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
        item = [QueryItem("test", "value")]
        return_list = ["test1", "test2"]
        basic_query = BasicQuery(item, return_list=return_list, operator="AND")
        generate_query = elastic_index_connector.generate_basic_query(basic_query)
        result = elastic_template_query
        result["query"]["query_string"]["query"] = "(test=value)"
        result["_source"] = return_list
        self.assertDictEqual(generate_query, result)

    def test__generate_basic_query__multi_query(self):
        elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
        item = [QueryItem("test", "value"), QueryItem("test_two", "test_two")]
        basic_query = BasicQuery(item, operator="AND")
        generate_query = elastic_index_connector.generate_basic_query(basic_query)
        result = elastic_template_query
        result["query"]["query_string"]["query"] = "((test=value) AND (test_two=test_two))"
        self.assertDictEqual(generate_query, result)

    def test__generate_basic_query_location__location(self):
        elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
        basic_query = BasicQuery([], table_name="test", collection_name="test")
        location_query = elastic_index_connector.generate_basic_query_location(basic_query)
        self.assertDictEqual(location_query, {
            "index": "test",
            "type": "test"
        })

    def test__generate_basic_query_location__basic_location(self):
        elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
        basic_query = BasicQuery([], table_name="test")
        location_query = elastic_index_connector.generate_basic_query_location(basic_query)
        self.assertDictEqual(location_query, {
            "index": "test",
        })

    def test__get_query_body__one_query(self):
        elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
        return_list = ["test1", "test2"]
        item = [QueryItem("test", "value"), QueryItem("test_two", "test_two")]
        basic_query = BasicQuery(item, return_list=return_list, operator="AND", table_name="test")
        advance_query = AdvanceQuery(basic_query)
        generate_query = elastic_index_connector.get_query_body(advance_query)
        data_query = elastic_template_query
        data_query["query"]["query_string"]["query"] = "((test=value) AND (test_two=test_two))"
        data_query["_source"] = return_list
        location = {
            "index": "test",
        }
        self.assertListEqual(generate_query, [location, data_query])


if __name__ == '__main__':
    unittest.main()
