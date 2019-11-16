from collections import defaultdict
from functools import partial

from QueryEngine.Parser.tagging_parser import get_group_by_key, is_keys_in_group, add_groups_extra_info
from QueryEngine.TaggingGroup import TaggingGroup


class TaggingEngine:
    def __init__(self, tagging_data):
        self.tagging_data = tagging_data.get_tagging_data()

    def get_tagging_groups(self, group_by):  # TODO: add stash system
        groups = defaultdict(TaggingGroup)
        for tagging_item in self.tagging_data:
            group_key = get_group_by_key(tagging_item, group_by)
            groups[group_key].add_item(tagging_item)
        return add_groups_extra_info(groups.values(), group_by)

    def get_relevant_tagging_groups(self, query_keys, group_by):
        groups = self.get_tagging_groups(group_by)
        partial_is_keys_in_group = partial(is_keys_in_group, query_keys)
        return filter(partial_is_keys_in_group, groups)
