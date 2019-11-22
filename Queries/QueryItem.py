class QueryItem:
    def __init__(self, key, value, options=None):
        self.key = key
        self.value = value
        self.options = options if options else dict()
