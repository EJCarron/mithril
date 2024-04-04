from .. import typesense_client
from .. import helpers
from src.scripts.data_wrangling import fetch_data
from src.objects.graph_objects.relationships import relationship_factory
from src.objects.graph_objects.nodes import node_factory


def get_regulated_entities(node_ids):
    config = helpers.get_config()

    nodes = fetch_data.get_nodes_of_type(node_ids=node_ids,
                                         node_type=node_factory.ec_regulated_entity_str, database=config.ec_database)

    return nodes


def get_donors(node_ids):
    config = helpers.get_config()
    nodes = fetch_data.get_nodes_of_type(node_ids=node_ids,
                                         node_type=node_factory.ec_donor_str, database=config.ec_database)

    return nodes


def get_nodes(node_ids):
    if len(node_ids) == 0:
        return []
    get_functions = [get_regulated_entities, get_donors]

    all_nodes = []

    for getter in get_functions:
        nodes = getter(node_ids)
        if nodes is None:
            continue
        all_nodes += nodes

    return all_nodes


def get_donors_by_company_number(company_number):
    config = helpers.get_config()

    query = f'select * from {node_factory.ec_donor_str} where' \
            f' "CompanyRegistrationNumber" in %s'
    nodes = fetch_data.execute_query(obj_type=node_factory.ec_donor_str, database=config.roi_database,
                                     params=[company_number], query=query)
    return nodes


def get_relationships(node_ids):
    config = helpers.get_config()

    donations = fetch_data.get_relationships(node_ids=node_ids,
                                             database=config.ec_database,
                                             relationship_type=relationship_factory.ec_donation_str)

    return donations


def search_typesense(query, page, search_type=None):
    if search_type is None:
        return search_typesense_all(query, page)
    elif search_type == node_factory.ec_regulated_entity_str:
        return search_typesense_regulated_entities(query, page)
    elif search_type == node_factory.ec_donor_str:
        return search_typesense_donors(query, page)


def search_typesense_all(query, page):
    regulate_entities = search_typesense_regulated_entities(query, page)
    donors = search_typesense_donors(query, page)

    results = regulate_entities + donors

    return results


def search_typesense_regulated_entities(query, page):
    results = typesense_client.paged_query(query=query, query_by='name',
                                           collection=node_factory.ec_regulated_entity_str,
                                           page=page)

    processed_results = []

    for result in results:
        doc = result['document']
        processed_result = {'title': doc['name'],
                            'name': doc['name'],
                            'node_id': doc['node_id'],
                            'init_token': doc['node_id'],
                            'display_description': doc['RegulatedEntityType'],
                            'node_type': node_factory.ec_regulated_entity_str
                            }
        processed_results.append(processed_result)
    return processed_results


def search_typesense_donors(query, page):
    results = typesense_client.paged_query(query=query, query_by='name',
                                           collection=node_factory.ec_donor_str,
                                           page=page)

    processed_results = []

    for result in results:
        doc = result['document']
        processed_result = {
            'title': doc['name'],
            'name': doc['name'],
            'node_id': doc['node_id'],
            'init_token': doc['node_id'],
            'display_description': doc['DonorStatus'],
            'node_type': node_factory.ec_donor_str
        }
        processed_results.append(processed_result)
    return processed_results


def find_matches(search_dicts):
    return typesense_client.find_matches(search_dicts)
