import requests


class ApiConfig:
    def __init__(self, url_config):
        self.tagging_url = url_config.get('tagging_url')
        self.ontology_url = url_config.get('ontology_url')

    def get_tagging_data(self):
        return requests.get(self.tagging_url)

    def get_ontology_data(self):
        return requests.get(self.ontology_url)
