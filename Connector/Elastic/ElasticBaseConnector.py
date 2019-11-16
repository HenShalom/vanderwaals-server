from elasticsearch import Elasticsearch
from typing import Union

from Connector.BaseConnector import BaseConnector
from const import RETURN_ALL
from Queries.QueryItem import QueryItem
from Queries.BasicQuery import BasicQuery


class ElasticBaseConnector(BaseConnector):
    def __init__(self, schema):
        BaseConnector.__init__(self, schema)
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
    def extract_row(result: dict) -> list:
        return result.get('hits', {}) \
            .get('hits', [])
