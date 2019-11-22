def filter_empty_queries(query_list):
    return list(filter(lambda x: x is not None, query_list))
