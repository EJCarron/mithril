from .. import helpers
import psycopg2
from .. import typesense_client

def connect_to_db():
    config = helpers.get_config()

    conn = psycopg2.connect(database=config.ol_database,
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


def find_matches(search_dicts):
    return typesense_client.find_matches(search_dicts)


