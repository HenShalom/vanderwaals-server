import json


class DocumentLoader:
    def __init__(self, location):
        self.location = location

    def get_data(self):
        with open(self.location) as file:
            return json.load(file)
