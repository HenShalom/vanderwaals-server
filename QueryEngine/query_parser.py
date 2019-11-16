from functools import reduce


def extract_ontology_field(query: dict):
    if query.get("fields"):
        return reduce(lambda prev, sub_query: prev + extract_ontology_field(sub_query), query.get("fields"), [])
    return [query]


def extract_ontology_keys(query):
    query_fields = extract_ontology_field(query)
    return {field.get("key"): field.get("optional", False) for field in query_fields}
