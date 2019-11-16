from QueryEngine.TaggingGroup import TaggingGroup

from const import GROUP_DELIMITER, BDT_KEY


def get_tagging_settings(tagging_item: dict, group_by: list):
    group_item = tagging_item
    return {group_by_item: group_item[group_by_item] for group_by_item in group_by}


def add_initial_settings_to_groups(groups, group_by):
    for group in groups:
        settings = get_tagging_settings(group.tagging_items[0], group_by)
        group.update_settings(settings)
    return groups


def get_group_by_key(tagging_item, group_by):
    return GROUP_DELIMITER.join([tagging_item.get(key, "None") for key in group_by])


def get_groups_keys(group: TaggingGroup) -> set:
    return {group_item.get(BDT_KEY) for group_item in group.tagging_items}


def is_keys_in_group(keys: dict, group: TaggingGroup):
    group_keys = get_groups_keys(group)
    for key, is_optional in keys.items():
        if not (is_optional or key in group_keys):
            return False
    return True
