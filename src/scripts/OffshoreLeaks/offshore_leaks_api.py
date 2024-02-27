from .. import helpers
import psycopg2
import typesense


def connect_to_db():
    config = helpers.get_config()

    conn = psycopg2.connect(database=config.database,
                            host=config.database_host,
                            user=config.database_user,
                            password=config.database_pw,
                            port=config.database_port)

    return conn


def render_select_nodes_query(table, node_ids):
    node_ids = [str(node_id) for node_id in node_ids]
    nodes = '(' + ','.join(node_ids) + ')'

    return f'SELECT * FROM {table} where db_node_id in{nodes}'


def execute_get_nodes_query(query, node_type):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    raw_nodes = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    if raw_nodes is None:
        return None

    nodes = []

    for raw_node in raw_nodes:
        node = {}
        for i in range(len(column_names)):
            node[column_names[i]] = raw_node[i]
        node['node_type'] = node_type
        nodes.append(node)

    return nodes


# def execute_get_matches_query(query):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     cursor.execute(query)
#     raw_results = cursor.fetchall()
#     column_names = [desc[0] for desc in cursor.description]
#
#     if raw_results is None:
#         return None
#
#     matches = []
#
#     for raw_result in raw_results:
#         result = {}
#         for i in range(len(column_names)):
#             result[column_names[i]] = raw_result[i]
#
#         matches.append(result)
#
#     return matches


def get_nodes_of_type(node_ids, table, node_type):
    query = render_select_nodes_query(table=table, node_ids=node_ids)
    nodes = execute_get_nodes_query(query, node_type)
    return nodes


def get_addresses(node_ids):
    config = helpers.get_config()
    nodes = get_nodes_of_type(node_ids=node_ids, table=config.database_addresses_table,
                              node_type='OffshoreLeaksAddress')
    return nodes


def get_entities(node_ids):
    config = helpers.get_config()
    nodes = get_nodes_of_type(node_ids=node_ids, table=config.database_entities_table, node_type='OffshoreLeaksEntity')
    return nodes


def get_intermediaries(node_ids):
    config = helpers.get_config()
    nodes = get_nodes_of_type(node_ids=node_ids, table=config.database_intermediaries_table,
                              node_type='OffshoreLeaksIntermediary')
    return nodes


def get_officers(node_ids):
    config = helpers.get_config()
    nodes = get_nodes_of_type(node_ids=node_ids, table=config.database_officers_table, node_type='OffshoreLeaksOfficer')
    return nodes


def get_others(node_ids):
    config = helpers.get_config()
    nodes = get_nodes_of_type(node_ids=node_ids, table=config.database_others_table, node_type='OffshoreLeaksOther')
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


def get_relationships(db_node_id):
    config = helpers.get_config()
    query = 'SELECT * FROM {table} WHERE node_id_start={node_id} or node_id_end={node_id}'.format(
        table=config.database_relationships_table, node_id=db_node_id)

    nodes = execute_get_nodes_query(query, 'OffshoreLeaksRelationship')

    return nodes


def clean_for_fuzz(name):
    strip_strings = ['plc', 'ltd', 'limited', 'llp', 'co.', '.', ',', ':', ';', '(', ')']

    name = name.lower()

    for stripper in strip_strings:
        name = name.replace(stripper, '')

    name = name.strip()

    return name


# def render_fuzz_match_query(node_dicts):
#     config = helpers.get_config()
#
#     searches = []
#
#     for node in node_dicts:
#         node['fuzz_name'] = clean_for_fuzz(node['name'])
#
#         def render_search(node_type, node_name, fuzz_name, node_id, fuzz_threshold):
#             return f"""
#                 \n
#                 insert into potentialMatches
#                 SELECT '{node_type}', db_node_id , original_name, '{node_name}', '{node_id}',
#                 levenshtein('{fuzz_name}', fuzz_name)
#                 from {config.fuzzy_table}
#                 where levenshtein('{fuzz_name}', fuzz_name) < {fuzz_threshold};
#                 \n
#                 """
#
#         searches.append(render_search(node_type=node['node_type'], node_name=node['fuzz_name'],
#                                       node_id=node['node_id'],
#                                       fuzz_threshold=3
#                                       ))
#
#     search_statements = ''.join(searches)
#
#     query = """
#         create temp table potentialMatches(node_type text,
#         match_node_id text, match_node_name text, compare_node_name text, compare_node_id text, fuzz int);
#
#         {search_statements}
#
#         select * from potentialMatches order by fuzz;
#
#         drop table potentialMatches;
#
#         """.format(search_statements=search_statements)
#
#     return query


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


def make_typesense_search_parameters(query_string, query_by):
    search_parameters = {
        'q': f'{query_string}',
        'query_by': f'{query_by}'
    }
    return search_parameters


def search_typesense_db(client, search, collection):
    response = client.collections[collection].documents.search(search)

    return response


# cannot feed script node objects, so nodes given to search against must be list of dicts.
# The Dicts only have to have node_id and node_name to cross-reference against
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
