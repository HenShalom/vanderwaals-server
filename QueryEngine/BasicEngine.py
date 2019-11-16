from QueryEngine import TaggingEngine
from QueryEngine.Parser.query_parser import extract_ontology_keys
from QueryEngine.quey_builder import generate_basic_queries, create_advance_queries
from const import DEFAULT_GROUP_BY


class BasicEngine:
    def __init__(self, connectors, tagging_loader):
        self.connectors = connectors
        self.tagging_loader = tagging_loader
        self.tagging_loader.init_data()
        self.tagging_engine = TaggingEngine(self.tagging_loader)

    def process_results(self, result):
        return result

    def execute_queries(self, advance_queries):
        all_results = []
        for query in advance_queries:  # TODO: make async await
            result = self.connectors[query.schema_name].query_data(query)
            all_results += self.process_results(result)
        return all_results

    def query(self, query):
        group_by = query.get("options", {}).get("groupBy", DEFAULT_GROUP_BY)
        queries_key = extract_ontology_keys(query)
        relevant_tagging_groups = self.tagging_engine.get_relevant_tagging_groups(queries_key, group_by)
        basic_queries = [generate_basic_queries(query, group) for group in relevant_tagging_groups]
        advance_queries = create_advance_queries(basic_queries)
        return self.execute_queries(advance_queries)
