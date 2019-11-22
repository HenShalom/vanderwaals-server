from typing import List

from Queries import AdvanceQuery, BasicQuery
from QueryEngine import TaggingGroup
from QueryEngine.Parser.query_parser import generate_basic_query


def generate_basic_queries(query: dict, group: TaggingGroup):
    basic_query = generate_basic_query(query, group)
    if not basic_query: return None
    settings = group.settings
    basic_query.return_list = list(group.keys_dict.values())
    basic_query.table_name = settings.get("table", ""),
    basic_query.collection_name = settings.get("collection", "")
    basic_query.schema_name = settings.get("schema", "")
    return basic_query


def create_advance_queries(basic_queries: List[BasicQuery]):
    advance_queries = dict()
    for basic_query in basic_queries:
        schema_name = basic_query.schema_name
        if not advance_queries.get(schema_name):
            advance_queries[schema_name] = AdvanceQuery([], schema_name=schema_name)
        advance_queries[schema_name].add_query(basic_query)
    return advance_queries.values()
