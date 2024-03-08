from ..OffshoreLeaks import offshore_leaks_api
from ..uk_electoral_commission import electoral_commission_api
from src.objects.graph_objects.nodes import node_factory


def find_potential_connections_in_offshore_leaks_db(network):
    search_dicts = create_offshore_leaks_matches_search_dicts(network)

    potential_matches = offshore_leaks_api.find_matches(search_dicts)

    return potential_matches


def find_potential_electoral_commission_donation_matches(network):
    search_dicts = create_electoral_commission_donation_matches_search_dicts(network)

    potential_matches = electoral_commission_api.find_matches(search_dicts)

    return potential_matches


def add_electoral_commission_donation_connections_to_network(matches, network):
    new_node_ids = []
    for match in matches:
        compare_node = network.get_node(match['info']['compare_node_id'])

        if network.node_in_network(match['values']['node_id']):
            new_ec_node = network.get_node(match['values']['node_id'])
        else:
            new_ec_node_dict = electoral_commission_api.get_donors(node_ids=[match['values']['node_id']])[0]
            new_ec_node = node_factory.node_dict[new_ec_node_dict['node_type']](**new_ec_node_dict)
            network.add_node(new_ec_node, node_factory.ec_node)

        network.create_same_as_relationship(parent_node_id=compare_node.node_id, child_node_id=new_ec_node.node_id)
        new_node_ids.append(new_ec_node.node_id)

    network.expand_network(target_node_ids=new_node_ids)

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


def create_electoral_commission_donation_matches_search_dicts(network):
    nodes = network.get_nodes_of_type(node_factory.ec_node, inverse=True)

    search_dicts = []

    for node in nodes.values():
        search_dicts.append(make_search_dict(query_string=node.name, query_by='name', collection='donors',
                                             node_id=node.node_id, node_name=node.name
                                             ))
        search_dicts.append(make_search_dict(query_string=node.name, query_by='name', collection='regulated_donees',
                                             node_id=node.node_id, node_name=node.name
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
