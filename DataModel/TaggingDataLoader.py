from DataModel.helpers import init_data_getter


class TaggingDataLoader:
    def __init__(self, tagging_config, ontology_config):
        self.tagging_data = []
        self.ontology_data = dict()
        self.tagging_data_getter = init_data_getter(tagging_config)
        self.ontology_data_getter = init_data_getter(ontology_config)

    def init_data(self):
        self.tagging_data = self.tagging_data_getter.get_data()
        self.ontology_data = self.ontology_data_getter.get_data()

    def get_tagging_data(self):
        return self.tagging_data

    def get_ontology_data(self):
        return self.ontology_data


if __name__ == '__main__':
    print("test")
