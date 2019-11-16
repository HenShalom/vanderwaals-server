import operator
from functools import reduce


def get_from_dict(data_dict: dict, map_list: list):
    return reduce(operator.getitem, map_list, data_dict)
