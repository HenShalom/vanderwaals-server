from DataModel.helpers import init_data_getter


class SchemaLoader:
    def __init__(self, schema_config):
        self.schema = dict()
        self.schema_getter = init_data_getter(schema_config)

    def init_data(self):
        self.schema = self.schema_getter.get_data()

    def get_schema(self):
        return self.schema
