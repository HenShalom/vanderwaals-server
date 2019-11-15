import requests


class DocumentLoader:
    def __init__(self, location):
        self.location = location

    def get_data(self):
        raise NotImplementedError()
