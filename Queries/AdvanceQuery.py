class AdvanceQuery:
    def __init__(self, basic_queries=list, schema_name=None):
        self.basic_queries = basic_queries if isinstance(basic_queries, list) else [basic_queries]
        self.schema_name = schema_name

    def add_query(self, query):
        self.basic_queries.append(query)
