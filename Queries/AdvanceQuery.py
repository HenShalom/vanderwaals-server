class AdvanceQuery:
    def __init__(self, connector, basic_queries):
        self.basic_queries = basic_queries if isinstance(basic_queries, list) else [basic_queries]
        self.connector = connector

    def add_query(self, query):
        self.basic_queries.append(query)
