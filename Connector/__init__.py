from Connector.Elastic.ElasticMultiIndexConnector import ElasticMultiIndexConnector
from Connector.Elastic.ElasticSingleIndexConnector import ElasticSingleIndexConnector

connector_dict = {
    "elastic": {
        "single_index": ElasticSingleIndexConnector,
        "multi_index": ElasticMultiIndexConnector
    }
}
