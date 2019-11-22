from functools import reduce

from QueryEngine.utiles import filter_empty_queries
from Queries import QueryItem, BasicQuery
from QueryEngine import TaggingGroup
from const import AND_OPERATOR


def extract_ontology_field(query: dict):
    if query.get("fields"):
        return reduce(lambda prev, sub_query: prev + extract_ontology_field(sub_query), query.get("fields"), [])
    return [query]


def extract_ontology_keys(query):
    query_fields = extract_ontology_field(query)
    return {field.get("key"): field.get("optional", False) for field in query_fields}


def generate_query_item(query_item_dict: dict, group: TaggingGroup):
    if group.keys_dict.get(query_item_dict.get("key")):
        return QueryItem(
            group.keys_dict.get(query_item_dict.get("key")),
            query_item_dict.get("value"),
            query_item_dict.get("advance")
        )
    return None


def generate_basic_query_query_items(query_dict: dict, group: TaggingGroup) -> list:
    query_items = [generate_basic_query(query, group) for query in query_dict.get("fields")]
    return filter_empty_queries(query_items)


def generate_basic_query(query_dict: dict, group: TaggingGroup):
    if query_dict.get("fields"):
        query_items = generate_basic_query_query_items(query_dict, group)
        if len(query_items) == 0: return None
        return BasicQuery(query_items=query_items,
                          operator=query_dict.get("operator", AND_OPERATOR))
    return generate_query_item(query_dict, group)
