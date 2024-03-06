from ..OffshoreLeaks import offshore_leaks_api
from ..uk_electoral_commission import registered_interests_api
from src.objects.graph_objects.nodes import node_factory


def find_potential_connections_in_offshore_leaks_db(network):
    search_dicts = create_offshore_leaks_matches_search_dicts(network)

    potential_matches = offshore_leaks_api.find_matches(search_dicts)

    return potential_matches


def find_potential_registered_interests_matches(network):
    search_dicts = create_registered_interests_matches_search_dicts(network)

    potential_matches = registered_interests_api.find_matches_grouped(search_dicts)

    return potential_matches


def add_registered_interests_connections_to_network(matches, network):
    for match in matches:
        kwargs = {}

        for key, value in match['values'].items():
            new_key = key.replace(' ', '_').lower()
            kwargs[new_key] = value

        node = node_factory.regulated_donee(name=kwargs['regulated_donee'])

        network.add_regulated_donee(node)

        network.create_registered_interest_relationship(parent_node_id=match['info']['compare_node_id'],
                                             child_node_id=node.node_id,
                                             attributes=kwargs)

    return network


def add_offshore_leaks_connections_to_network(matches, network):
    for match in matches:

        match['values']['db_node_id'] = match['values']['node_id']
        del match['values']['node_id']
        del match['values']['id']

        if match['info']['collection'] == 'entities':
            node = node_factory.ol_entity(**match['values'])
        elif match['info']['collection'] == 'officers':
            node = node_factory.ol_officer(**match['values'])
        elif match['info']['collection'] == 'addresses':
            node = node_factory.ol_address(**match['values'])
        elif match['info']['collection'] == 'others':
            node = node_factory.ol_other(**match['values'])
        else:
            print('SYSTEM ERROR match collection not valid ' + match['info']['collection'])
            continue
        network.add_ol_node(node)

        network.create_same_as_relationship(parent_node_id=match['info']['compare_node_id'], child_node_id=node.node_id)

    return network


def create_registered_interests_matches_search_dicts(network):
    ch_companies = network.ch_companies.values()
    ch_officers = network.ch_officers.values()

    nodes = list(ch_officers) + list(ch_companies)

    search_dicts = []

    for node in nodes:
        search_dicts.append(make_search_dict(query_string=node.name, query_by='Donor', collection='donations',
                                             node_id=node.node_id, node_name=node.name, group_by='Donor'
                                             ))

    return search_dicts


def make_search_dict(query_string, query_by, collection, node_id, node_name, group_by=None):

    search_dict = {
        'params': make_typesense_search_parameters(query_string=query_string, query_by=query_by, group_by=group_by),
        'collection': collection,
        'node_id': node_id,
        'node_name': node_name,
    }

    return search_dict


def make_typesense_search_parameters(query_string, query_by, group_by=None):
    search_parameters = {
        'q': f'{query_string}',
        'query_by': f'{query_by}'
    }

    if group_by is not None:
        search_parameters['group_by'] = group_by

    return search_parameters


def create_offshore_leaks_matches_search_dicts(network):
    ch_companies = network.ch_companies
    ch_officers = network.ch_officers

    search_dicts = []

    search_by_name_collections = ['entities', 'officers', 'intermediaries', 'others']

    def make_search_by_name_dict(node, _collection):
        search_dicts.append(
            make_search_dict(query_string=node.name, query_by='name',
                             collection=_collection, node_id=node.node_id, node_name=node.name
                             ))

    for ch_company in ch_companies.values():
        for collection in search_by_name_collections:
            make_search_by_name_dict(ch_company, collection)

        search_dicts.append(
            make_search_dict(query_string=ch_company.address, query_by='address',
                             collection='addresses', node_id=ch_company.node_id, node_name=ch_company.name
                             ))

    for ch_officer in ch_officers.values():
        for collection in search_by_name_collections:
            make_search_by_name_dict(ch_officer, collection)

    return search_dicts
