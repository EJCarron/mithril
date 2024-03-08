import typesense
import pprint


def make_typesense_client():
    client = typesense.Client({
        'nodes': [{
            'host': 'localhost',
            'port': '8108',
            'protocol': 'http'
        }],
        'api_key': 'xyz',
        'connection_timeout_seconds': 20
    })
    return client


def search_typesense_db(client, search, collection):
    response = client.collections[collection].documents.search(search)

    return response


def find_matches_grouped(search_dicts):
    client = make_typesense_client()

    results = []

    for search_dict in search_dicts:
        response = search_typesense_db(client=client, search=search_dict['params'],
                                       collection=search_dict['collection']
                                       )

        if response is not None:
            for group_hit in response['grouped_hits']:
                group_hit['group_key'] = group_hit['group_key'][0]
                result = {'values': group_hit, 'info': {}}
                result['info']['collection'] = search_dict['collection']
                result['info']['compare_node_id'] = search_dict['node_id']
                result['info']['compare_node_name'] = search_dict['node_name']
                result['info']['matched_to'] = search_dict['params']['q']
                result['info']['searched_by'] = search_dict['params']['query_by']
                results.append(result)

    return results


def db_report():
    client = make_typesense_client()

    collections = client.collections.retrieve()
    for collection in collections:
        pprint.pprint(collection)
    for collection in collections:
        print('---------------------------------------------------------')
        name = collection['name'].upper()
        docs = collection['num_documents']
        print(f'{name}:  {docs}')



def find_matches(search_dicts):
    client = make_typesense_client()

    results = []

    for search_dict in search_dicts:
        response = search_typesense_db(client=client, search=search_dict['params'],
                                       collection=search_dict['collection'])
        if response is not None:

            for hit in response['hits']:
                result = {'values': hit['document'], 'info': {}}
                result['info']['collection'] = search_dict['collection']
                result['info']['compare_node_id'] = search_dict['node_id']
                result['info']['compare_node_name'] = search_dict['node_name']
                result['info']['matched_to'] = search_dict['params']['q']
                result['info']['searched_by'] = search_dict['params']['query_by']
                results.append(result)

    return results
