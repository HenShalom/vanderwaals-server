from DataModel.DataLoaders.ApiLoader import ApiConfig
from DataModel.DataLoaders.DocumentLoader import DocumentLoader


class DataLoader:
    def __init__(self, **args):
        if args.get('url_config'):
            self.data_getter = ApiConfig(args.get('url_config'))
        if args.get('file_config'):
            self.data_getter = DocumentLoader(args.get('file_config'))

    def init_data(self):
        self.tagging_data = self.data_getter.get_tagging_data()
        self.ontology_data = self.data_getter.get_ontology_data()

    def get_tagging_data(self):
        return self.tagging_data

    def get_ontology_data(self):
        return self.ontology_data
