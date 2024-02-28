import typesense


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
