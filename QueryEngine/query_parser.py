from functools import reduce
from Queries import QueryItem, BasicQuery
from const import AND_OPERATOR


def extract_ontology_field(query: dict):
    if query.get("fields"):
        return reduce(lambda prev, sub_query: prev + extract_ontology_field(sub_query), query.get("fields"), [])
    return [query]


def extract_ontology_keys(query):
    query_fields = extract_ontology_field(query)
    return {field.get("key"): field.get("optional", False) for field in query_fields}


def generate_query_item(query_item_dict):
    return QueryItem(
        query_item_dict.get("key"),
        query_item_dict.get("value"),
        query_item_dict.get("advance")
    )


def generate_basic_query(query_dict):
    if query_dict.get("fields"):
        return BasicQuery(query_items=[generate_basic_query(query) for query in query_dict.get("fields")],
                          operator=query_dict.get("operator", AND_OPERATOR))
    return generate_query_item(query_dict)
