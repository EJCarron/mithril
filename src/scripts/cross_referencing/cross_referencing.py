from ..OffshoreLeaks import offshore_leaks_api
from src.objects.graph_objects.nodes import node_factory
from .. import helpers


# cannot feed script node objects, so nodes given to search against must be list of dicts.
# The Dicts only have to have node_id and node_name to cross-reference against
def find_potential_connections_in_offshore_leaks_db(network):
    search_dicts = create_offshore_leaks_matches_search_dicts(network)

    potential_matches = offshore_leaks_api.find_matches(search_dicts)

    return potential_matches


def make_search_dict(params, collection, node_id, node_name):
    return {
        'params': params,
        'collection': collection,
        'node_id': node_id,
        'node_name': node_name,
    }


def create_offshore_leaks_matches_search_dicts(network):
    ch_companies = network.ch_companies
    ch_officers = network.ch_officers

    search_dicts = []

    for ch_company in ch_companies.values():
        search_dicts.append(
            make_search_dict(params=offshore_leaks_api.make_typesense_search_parameters(query_string=ch_company.name,
                                                                                        query_by='name'),
                             collection='entities', node_id=ch_company.node_id, node_name=ch_company.name

                             ))

        search_dicts.append(
            make_search_dict(params=offshore_leaks_api.make_typesense_search_parameters(query_string=ch_company.name,
                                                                                        query_by='name'),
                             collection='officers', node_id=ch_company.node_id, node_name=ch_company.name

                             ))
        search_dicts.append(
            make_search_dict(params=offshore_leaks_api.make_typesense_search_parameters(query_string=ch_company.name,
                                                                                        query_by='name'),
                             collection='intermediaries', node_id=ch_company.node_id, node_name=ch_company.name

                             ))
        search_dicts.append(
            make_search_dict(params=offshore_leaks_api.make_typesense_search_parameters(query_string=ch_company.name,
                                                                                        query_by='name'),
                             collection='others', node_id=ch_company.node_id, node_name=ch_company.name

                             ))
        search_dicts.append(
            make_search_dict(params=offshore_leaks_api.make_typesense_search_parameters(query_string=ch_company.address,
                                                                                        query_by='name'),
                             collection='addresses', node_id=ch_company.node_id, node_name=ch_company.name

                             ))

    for ch_officer in ch_officers.values():
        search_dicts.append(
            make_search_dict(params=offshore_leaks_api.make_typesense_search_parameters(query_string=ch_officer.name,
                                                                                        query_by='name'),
                             collection='entities', node_id=ch_officer.node_id, node_name=ch_officer.name

                             ))

        search_dicts.append(
            make_search_dict(params=offshore_leaks_api.make_typesense_search_parameters(query_string=ch_officer.name,
                                                                                        query_by='name'),
                             collection='officers', node_id=ch_officer.node_id, node_name=ch_officer.name

                             ))
        search_dicts.append(
            make_search_dict(params=offshore_leaks_api.make_typesense_search_parameters(query_string=ch_officer.name,
                                                                                        query_by='name'),
                             collection='intermediaries', node_id=ch_officer.node_id, node_name=ch_officer.name

                             ))
        search_dicts.append(
            make_search_dict(params=offshore_leaks_api.make_typesense_search_parameters(query_string=ch_officer.name,
                                                                                        query_by='name'),
                             collection='others', node_id=ch_officer.node_id, node_name=ch_officer.name

                             ))

    return search_dicts
