from const import RETURN_ALL, AND_OPERATOR


class BasicQuery:
    def __init__(self, query_items, table_name=None, collection_name=None,
                 operator=AND_OPERATOR,
                 return_list=RETURN_ALL):
        self.operator = operator
        self.query_items = query_items if isinstance(query_items, list) else [query_items]
        self.table_name = table_name
        self.collection_name = collection_name
        self.return_list = return_list

    def __add__(self, basic_query):
        query_items = basic_query.query_items + self.query_items
        return BasicQuery(query_items, table_name=self.table_name, collection_name=self.collection_name,
                          return_list=self.return_list, operator=self.operator)
