from functools import reduce
from typing import Union, List
from const import RETURN_ALL
from elasticsearch import Elasticsearch
from Queries.QueryItem import QueryItem
from Queries.AdvanceQuery import AdvanceQuery
from Queries.BasicQuery import BasicQuery


class ElasticSingleIndexConnector:
    def __init__(self, schema):
        self.schema = schema
        self.es = Elasticsearch(self.schema.get("connection").get("hosts"),
                                **self.schema.get("connection").get("elasticOption", {}))

    def generate_query_item(self, query_item: Union[BasicQuery, QueryItem]):
        if isinstance(query_item, QueryItem):
            return "({}={})".format(query_item.key, query_item.value)
        delimiter_spacer = " {} ".format(query_item.operator)
        queries = delimiter_spacer.join(map(self.generate_query_item, query_item.query_items))
        if len(query_item.query_items) == 1:
            return "{}".format(queries)
        return "({})".format(queries)

    def generate_basic_query(self, basic_query: BasicQuery) -> dict:
        string_query = self.generate_query_item(basic_query)
        query = {
            "query": {
                "query_string": {
                    "query": string_query
                }
            }
        }
        if not basic_query.return_list == RETURN_ALL:
            query["_source"] = basic_query.return_list
        return query

    @staticmethod
    def generate_basic_query_location(basic_query: BasicQuery) -> dict:
        if basic_query.collection_name and basic_query.table_name:
            return {
                "index": basic_query.collection_name,
                "type": basic_query.collection_name
            }
        return {
            "index": basic_query.table_name,
        }

    def get_query_body(self, advance_query: AdvanceQuery) -> List[dict]:
        body = []
        for basic_query in advance_query.basic_queries:
            body.append(self.generate_basic_query_location(basic_query))
            body.append(self.generate_basic_query(basic_query))
        return body

    @staticmethod
    def extract_row(result: dict) -> list:
        return result.get('hits', {}) \
            .get('hits', [])

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
