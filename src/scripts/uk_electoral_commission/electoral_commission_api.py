from .. import typesense_client
from .. import helpers
import psycopg2


def connect_to_db():
    config = helpers.get_config()

    conn = psycopg2.connect(database=config.roi_database,
                            host=config.database_host,
                            user=config.database_user,
                            password=config.database_pw,
                            port=config.database_port)

    return conn


def render_select_nodes_query(table, node_ids):
    node_ids = [f'\'{node_id}\'' for node_id in node_ids]
    nodes = '(' + ','.join(node_ids) + ')'

    return f'SELECT * FROM {table} where node_id in {nodes}'


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


def get_nodes_of_type(node_ids, table, node_type):
    query = render_select_nodes_query(table=table, node_ids=node_ids)
    nodes = execute_get_nodes_query(query, node_type)
    return nodes


def get_regulated_donees(node_ids):
    config = helpers.get_config()
    return get_nodes_of_type(node_ids=node_ids, table=config.roi_database_regulated_donees_table,
                             node_type='ElectoralCommissionRegulatedDonee')


def get_donors(node_ids):
    config = helpers.get_config()
    return get_nodes_of_type(node_ids=node_ids, table=config.roi_database_donors_table, node_type='ElectoralCommissionDonor')


def get_nodes(node_ids):
    get_functions = [get_regulated_donees, get_donors]

    all_nodes = []

    for getter in get_functions:
        nodes = getter(node_ids)
        if nodes is None:
            continue
        all_nodes += nodes

    return all_nodes


def get_donations(node_id):
    config = helpers.get_config()
    query = f'SELECT * FROM {config.roi_database_donations_table} WHERE regulated_donee_node_id=\'{node_id}\' ' \
            f'or donor_node_id=\'{node_id}\''

    nodes = execute_get_nodes_query(query, 'ElectoralCommissionDonation')

    return nodes


def find_matches(search_dicts):
    return typesense_client.find_matches(search_dicts)

