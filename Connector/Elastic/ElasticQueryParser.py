from typing import Union

from const import FIXED_FIELD, AND_OPERATOR
from Connector.Elastic.consts import MATCH, TERM, AND_QUERY, OR_QUERY
from Queries.QueryItem import QueryItem
from Queries.BasicQuery import BasicQuery


def parse_query_item(query_item: QueryItem) -> dict:
    query_term = TERM if query_item.options.get(FIXED_FIELD) else MATCH
    return {
        query_term: {
            query_item.key: query_item.value
        }
    }


def parse_basic_query(basic_query: Union[BasicQuery, QueryItem]) -> dict:
    if isinstance(basic_query, QueryItem):
        return parse_query_item(basic_query)
    operator_value = AND_QUERY if basic_query.operator == AND_OPERATOR else OR_QUERY
    return {
        operator_value: list(map(parse_basic_query, basic_query.query_items))
    }
