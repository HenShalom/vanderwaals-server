class TaggingGroup:
    def __init__(self, tagging_items, settings):
        self.tagging_items = tagging_items
        self.settings = settings

    def add_item(self, tagging_item):
        self.tagging_items.append(tagging_item)

    def update_settings(self, settings):
        self.settings = settings
