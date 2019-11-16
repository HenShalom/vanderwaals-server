class TaggingGroup:
    def __init__(self, tagging_items=None, settings=None, keys_dict=None):
        self.tagging_items = tagging_items if tagging_items else []
        self.settings = settings
        self.keys_dict = keys_dict

    def add_item(self, tagging_item):
        self.tagging_items.append(tagging_item)

    def update_settings(self, settings):
        self.settings = settings

    def update_keys_dict(self, keys_dict):
        self.keys_dict = keys_dict
