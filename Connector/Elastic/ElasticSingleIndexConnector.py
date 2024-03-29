from functools import reduce
from typing import List

from const import FIXED_FIELD, TABLE_FIELD, COLLECTION_FIELD
from Connector.Elastic.consts import SOURCE_KEY
from Connector.Elastic.ElasticBaseConnector import ElasticBaseConnector
from Queries.QueryItem import QueryItem
from Queries.AdvanceQuery import AdvanceQuery
from Queries.BasicQuery import BasicQuery


class ElasticSingleIndexConnector(ElasticBaseConnector):
    def __init__(self, schema):
        ElasticBaseConnector.__init__(self, schema)

    def generate_location_query_item(self, basic_query):
        location_query = []
        if self.schema.get("table_key"):
            table_query = QueryItem(self.schema.get("table_key"), basic_query.table_name, {FIXED_FIELD: True})
            location_query.append(table_query)
        if self.schema.get("collection_key"):
            collection_query = QueryItem(self.schema.get("collection_key"), basic_query.collection_name,
                                         {"fixed": True})
            location_query.append(collection_query)
        return BasicQuery(location_query)

    def generate_basic_query_location(self) -> dict:
        if self.schema.get("type"):
            return {
                "index": self.schema.get("index"),
                "type": self.schema.get("type")
            }
        return {
            "index": self.schema.get("index"),
        }

    def get_query_body(self, advance_query: AdvanceQuery) -> List[dict]:
        body = []
        for basic_query in advance_query.basic_queries:
            location_query = self.generate_location_query_item(basic_query)
            body.append(self.generate_basic_query_location())
            body.append(self.generate_basic_query(basic_query + location_query,
                                                  [self.schema.get("index"), self.schema.get("type")]))
        return body

    def parse_result(self, doc):
        basic_row = doc[SOURCE_KEY]
        if self.schema.get("table_key"):
            basic_row[TABLE_FIELD] = doc[self.schema.get("table_key")]
        if self.schema.get("collection_key"):
            basic_row[COLLECTION_FIELD] = doc[self.schema.get("collection_key")]
        return basic_row

    async def query_data(self, advance_query: AdvanceQuery):
        elastic_response = await self.es.msearch(body=self.get_query_body(advance_query))
        result_hits = map(self.extract_row, elastic_response.get("responses", []))
        all_results = reduce(lambda prev, value: prev + value, result_hits)
        return map(self.parse_result, all_results)
