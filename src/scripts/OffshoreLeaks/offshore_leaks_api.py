from .. import helpers
from .. import typesense_client
from src.scripts.data_wrangling import fetch_data
from src.objects.graph_objects.relationships import relationship_factory
from src.objects.graph_objects.nodes import node_factory
import json


def get_addresses(node_ids):
    config = helpers.get_config()
    nodes = fetch_data.get_nodes_of_type(node_ids=node_ids,
                                         node_type=node_factory.ol_address_str, database=config.ol_database)
    return nodes


def get_entities(node_ids):
    config = helpers.get_config()
    nodes = fetch_data.get_nodes_of_type(node_ids=node_ids, node_type=node_factory.ol_entity_str,
                                         database=config.ol_database)
    return nodes


def get_intermediaries(node_ids):
    config = helpers.get_config()
    nodes = fetch_data.get_nodes_of_type(node_ids=node_ids,
                                         node_type=node_factory.ol_intermediary_str, database=config.ol_database)
    return nodes


def get_officers(node_ids):
    config = helpers.get_config()
    nodes = fetch_data.get_nodes_of_type(node_ids=node_ids,
                                         node_type=node_factory.ol_officer_str,
                                         database=config.ol_database)
    return nodes


def get_others(node_ids):
    config = helpers.get_config()
    nodes = fetch_data.get_nodes_of_type(node_ids=node_ids, node_type=node_factory.ol_other_str,
                                         database=config.ol_database)
    return nodes


def get_nodes(node_ids):
    get_functions = [get_addresses, get_entities, get_intermediaries, get_officers, get_others]

    all_nodes = []

    for getter in get_functions:
        nodes = getter(node_ids)
        if nodes is None:
            continue
        all_nodes += nodes

    return all_nodes


def get_relationships(node_ids):
    config = helpers.get_config()

    relationships = fetch_data.get_relationships(node_ids=node_ids,
                                                 database=config.ol_database,
                                                 relationship_type=relationship_factory.ol_relationship_str)

    return relationships


def find_matches(search_dicts):
    return typesense_client.find_matches(search_dicts)


def process_results(results, node_type):
    processed_results = []

    for result in results:
        doc = result['document']

        source = doc['sourceID']

        display_description = f"""{source}
                                  {node_type}"""

        processed_result = {'title': doc['name'],
                            'name': doc['name'],
                            'node_id': doc['node_id'],
                            'init_token': doc['node_id'],
                            'display_description': display_description,
                            'node_type': node_type,
                            'full_description': json.dumps(doc, indent=4)
                            }
        processed_results.append(processed_result)

    return processed_results


def search_typesense(query, page_number, search_type=None):
    if search_type is None:
        parts = {ol_type: typesense_client.paged_query(query=query,
                                                       query_by='name',
                                                       collection=ol_type,
                                                       page=page_number
                                                       ) for ol_type in node_factory.ol_keys_dict.keys()}

        processed_results = []

        for ol_type, results in parts.items():
            processed_results += process_results(results, ol_type)

        return processed_results

    else:
        return process_results(typesense_client.paged_query(query=query,
                                                            query_by='name',
                                                            collection=search_type,
                                                            page=page_number
                                                            ), search_type)
