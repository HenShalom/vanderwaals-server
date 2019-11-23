from functools import reduce
from typing import List

from const import TABLE_FIELD
from Connector.Elastic.consts import INDEX_KEY, SOURCE_KEY
from Connector.Elastic.ElasticBaseConnector import ElasticBaseConnector
from Queries.QueryItem import QueryItem
from Queries.AdvanceQuery import AdvanceQuery
from Queries.BasicQuery import BasicQuery


class ElasticMultiIndexConnector(ElasticBaseConnector):
    def __init__(self, schema):
        ElasticBaseConnector.__init__(self, schema)

    @staticmethod
    def generate_basic_query_location(basic_query: BasicQuery) -> dict:
        # for multi index connector there is no option for collection
        return {
            "index": basic_query.table_name,
        }

    @staticmethod
    def parse_result(doc):
        return {
            TABLE_FIELD: doc[INDEX_KEY],
            **doc[SOURCE_KEY]
        }

    def get_query_body(self, advance_query: AdvanceQuery) -> List[dict]:
        body = []
        for basic_query in advance_query.basic_queries:
            body.append(self.generate_basic_query_location(basic_query))
            body.append(self.generate_basic_query(basic_query))
        return body

    async def query_data(self, advance_query: AdvanceQuery):
        elastic_response = await self.es.msearch(body=self.get_query_body(advance_query))
        result_hits = map(self.extract_row, elastic_response.get("responses", []))
        all_results = reduce(lambda prev, value: prev + value, result_hits)
        return map(self.parse_result, all_results)


if __name__ == '__main__':
    empty_schema = {
        "connection": {
            "hosts": ["http://localhost:9200"],
            "elasticOption": {
                "http_auth": ("elastic", "changeme")
            }
        }
    }
    elastic_index_connector = ElasticMultiIndexConnector(empty_schema)
    query_items = [QueryItem("id", "24")]
    basic_queries = BasicQuery(query_items, table_name="spotify-data")
    advance_query = AdvanceQuery(basic_queries)
