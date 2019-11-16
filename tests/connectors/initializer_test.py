import unittest
from Connector import ElasticSingleIndexConnector
from Connector.initializer import get_connector_class


class TestInitializer(unittest.TestCase):
    def test__get_connector_class(self):
        connector = get_connector_class("elastic.single_index")
        self.assertEqual(connector, ElasticSingleIndexConnector)
