import json
from DataModel import SchemaLoader, TaggingDataLoader
from Connector.initializer import initialize
from QueryEngine import BasicEngine

query = {
    "options": {
        "groupBy": [
            "schema",
            "table"
        ]
    },
    "operator": "AND",
    "fields": [
        {
            "key": "ID",
            "value": "24",
            "optional": True
        }
    ]
}


def main():
    schema_loader = SchemaLoader({"location": "./config/data/schema.json"})
    schema_loader.init_data()
    tagging_data = TaggingDataLoader({"location": "./config/data/tagging_data.json"},
                                     {"location": "./config/data/tagging_data.json"})
    schema_dict = initialize(schema_loader.schema)
    engine = BasicEngine(schema_dict, tagging_data)
    with open("./result.json", "w") as f:
        json.dump(engine.query(query), f)


if __name__ == '__main__':
    main()
