import requests


class ApiConfig:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        return requests.get(self.url).json()
