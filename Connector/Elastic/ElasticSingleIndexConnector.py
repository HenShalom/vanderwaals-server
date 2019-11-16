from functools import reduce
from typing import Union, List
from Connector.Elastic.ElasticBaseConnector import ElasticBaseConnector
from Queries.QueryItem import QueryItem
from Queries.AdvanceQuery import AdvanceQuery
from Queries.BasicQuery import BasicQuery


class ElasticSingleIndexConnector(ElasticBaseConnector):
    def __init__(self, schema):
        ElasticBaseConnector.__init__(self, schema)

    def get_query_body(self, advance_query: AdvanceQuery) -> List[dict]:
        body = []
        for basic_query in advance_query.basic_queries:
            body.append(self.generate_basic_query_location(basic_query))
            body.append(self.generate_basic_query(basic_query))
        return body

    def query_data(self, advance_query: AdvanceQuery):
        elastic_response = self.es.msearch(body=self.get_query_body(advance_query))
        result_hits = map(self.extract_row, elastic_response.get("responses", []))
        all_results = reduce(lambda prev, value: prev + value, result_hits)
        return map(lambda doc: doc["_source"], all_results)


if __name__ == '__main__':
    empty_schema = {
        "connection": {
            "hosts": ["http://localhost:9200"],
            "elasticOption": {
                "http_auth": ("elastic", "changeme")
            }
        }
    }

    elastic_index_connector = ElasticSingleIndexConnector(empty_schema)
    query_items = [QueryItem("id", "24")]
    basic_queries = BasicQuery(query_items, table_name="spotify-data")
    advance_query = AdvanceQuery(basic_queries)
