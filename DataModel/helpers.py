from DataModel.DataLoaders.ApiLoader import ApiConfig
from DataModel.DataLoaders.DocumentLoader import DocumentLoader


def init_data_getter(config):
    if config.get('url'):
        return ApiConfig(*config)
    if config.get('location'):
        return DocumentLoader(*config)
