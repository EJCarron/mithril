import typesense
import pprint
import json
import numpy as np
import pandas
import math as maths


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


def jsonline_stringify(list_of_objects):
    stringify = ''

    for obj in list_of_objects:
        stringify += json.dumps(obj) + '\n'

    return stringify


def split_df_to_size(df):
    df_size = df.memory_usage(index=True).sum()

    num_splits = maths.ceil(df_size / 1000000)

    split_dfs = np.array_split(df, num_splits)

    return split_dfs


def import_df(client, df, collection):
    dfs = split_df_to_size(df)
    print(collection)
    for df in dfs:
        df.fillna('NULL', inplace=True)
        client.collections[collection].documents.import_(
            jsonline_stringify(df.to_dict('records')).encode('utf-8'))


def paged_query(query, query_by, page, collection):
    client = make_typesense_client()

    params = {'q': query,
              'query_by': query_by,
              'page': page
              }

    response = search_typesense_db(client=client, search=params, collection=collection)

    if response is not None:
        return response['hits']
    else:
        return None


def find_matches(search_dicts):
    client = make_typesense_client()

    results = []

    for search_dict in search_dicts:
        q = search_dict['params']['q']
        collection = search_dict['collection']

        print(f'matching {q} against {collection}')
        response = search_typesense_db(client=client, search=search_dict['params'],
                                       collection=search_dict['collection'])
        if response is not None:

            for hit in response['hits']:
                hit['text_match_info']['score'] = int(hit['text_match_info']['score'])

                result = {'values': hit['document'], 'info': search_dict}
                result['info']['score'] = hit['text_match']
                results.append(result)

    def sort_func(e):
        return e['info']['score']

    results.sort(key=sort_func, reverse=True)

    result_counter = 0

    for result in results:
        result['values']['id'] = str(result_counter)
        result_counter += 1

    return results


def clear_typesense_cluster(you_are_sure=False):
    if you_are_sure:
        client = make_typesense_client()

        collections = client.collections.retrieve()

        [client.collections[collection['name']].delete() for collection in collections]


def drop_collection(collection):
    client = make_typesense_client()

    client.collections[collection].delete()
