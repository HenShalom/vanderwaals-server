from typing import List, Dict

from const import CONNECTOR_DELIMITER
from Connector import connector_dict
from Utiles import get_from_dict

from Connector.BaseConnector import BaseConnector


def get_connector_class(schema_connector: str):
    location = schema_connector.split(CONNECTOR_DELIMITER)
    return get_from_dict(connector_dict, location)


def initialize(schemas: List[dict]) -> Dict[str, BaseConnector]:
    schema_dict = dict()
    for schema in schemas:
        connector_class = get_connector_class(schema.get("connector_class"))
        schema_dict[schema.get("name")] = connector_class(schema)
    return schema_dict
