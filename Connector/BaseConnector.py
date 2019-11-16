from Queries import AdvanceQuery


class BaseConnector:
    def __init__(self, schema):
        self.schema = schema

    def query_data(self, advance_query: AdvanceQuery):
        raise NotImplementedError()
