empty_schema = {
    "index": "main_index",
    "connection": {
        "hosts": ["localhost:9200"],
    }
}

schema_with_table = {
    **empty_schema,
    "table_key": "_table"
}

schema_with_collection = {
    **empty_schema,
    "table_key": "_table",
    "collection_key": "_collection"
}

elastic_template_query = {
    "query": {
        "query_string": {
            "query": ""
        }
    }
}
