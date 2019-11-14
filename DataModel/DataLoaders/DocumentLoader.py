import requests


class DocumentLoader:
    def __init__(self, url):
        self.url = url

    def get_tagging_data(self):
        raise NotImplementedError()

    def get_ontology_data(self):
        raise NotImplementedError()
