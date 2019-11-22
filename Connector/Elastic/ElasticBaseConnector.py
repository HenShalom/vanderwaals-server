from elasticsearch_async import AsyncElasticsearch

from Connector.Elastic.ElasticQueryParser import parse_basic_query
from Connector.BaseConnector import BaseConnector
from const import RETURN_ALL
from Queries.BasicQuery import BasicQuery


class ElasticBaseConnector(BaseConnector):
    def __init__(self, schema):
        BaseConnector.__init__(self, schema)
        self.es = AsyncElasticsearch(self.schema.get("connection").get("hosts"),
                                     **self.schema.get("connection").get("elasticOption", {}))

    def generate_basic_query(self, basic_query: BasicQuery) -> dict:
        string_query = parse_basic_query(basic_query)
        query = {
            "query": {
                "bool": string_query
            }
        }
        print(query)
        if not basic_query.return_list == RETURN_ALL:
            query["_source"] = basic_query.return_list
        return query

    @staticmethod
    def extract_row(result: dict) -> list:
        return result.get('hits', {}) \
            .get('hits', [])
