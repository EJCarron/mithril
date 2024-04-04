from .. import helpers
import psycopg2


def connect_to_db(database):
    config = helpers.get_config()

    conn = psycopg2.connect(database=database,
                            host=config.database_host,
                            user=config.database_user,
                            password=config.database_pw,
                            port=config.database_port)

    return conn


def execute_query(query, params, obj_type, database):
    conn = connect_to_db(database)
    cursor = conn.cursor()

    params_tuple = tuple(params)

    cursor.execute(query, (params_tuple,))

    raw_results = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    if raw_results is None:
        return None

    results = []

    for raw_result in raw_results:
        result = {}
        for i in range(len(column_names)):
            result[column_names[i]] = raw_result[i]
        result['obj_type'] = obj_type
        results.append(result)

    return results

def get_nodes_of_type(node_ids, node_type, database):
    query = f'select * from {node_type} where {node_type}.node_id in %s'
    nodes = execute_query(obj_type=node_type, database=database, params=node_ids, query=query)
    return nodes


def get_relationships(node_ids, database, relationship_type):
    parent_query = f'select * from {relationship_type} where {relationship_type}.parent_node_id in %s'
    child_query = f'select * from {relationship_type} where {relationship_type}.child_node_id in %s'
    relationships = []

    relationships += execute_query(obj_type=relationship_type, database=database,
                                   params=node_ids, query=parent_query)

    relationships += execute_query(obj_type=relationship_type, database=database,
                                   params=node_ids, query=child_query)
    return relationships
