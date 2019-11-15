from const import RETURN_ALL


class BasicQuery:
    def __init__(self, table_name, collection_name, query_items, operator, return_list=RETURN_ALL):
        self.operator = operator
        self.query_items = query_items
        self.table_name = table_name
        self.collection_name = collection_name
        self.return_list = return_list
