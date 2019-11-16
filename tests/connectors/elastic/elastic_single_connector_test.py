import unittest
from tests.connector.elastic_common import elastic_template_query, empty_schema
from Connector.Elastic.ElasticSingleIndexConnector import ElasticSingleIndexConnector
from Queries.AdvanceQuery import AdvanceQuery
from Queries.BasicQuery import BasicQuery
from Queries.QueryItem import QueryItem


class TestElasticSingleIndex(unittest.TestCase):
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
