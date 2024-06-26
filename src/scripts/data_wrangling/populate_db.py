from src.scripts import helpers
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import psycopg2.extensions
from psycopg2.extras import execute_values
from src.scripts import typesense_client
from sqlalchemy.types import Text, Numeric
from src.scripts.generate_node_id import generate_node_id
from src.objects.graph_objects.nodes import node_factory
from src.objects.graph_objects.relationships import relationship_factory
import numpy

offshore_leaks_node_types = node_factory.ol_keys_dict.keys()

offshore_leaks_schemas = {node_factory.ol_entity_str: {
    'name': node_factory.ol_entity_str,
    'fields': [
        {'name': 'address', 'type': 'string'},
        {'name': 'name', 'type': 'string'},
        {'name': 'original_name', 'type': 'string'},
        {'name': 'former_name', 'type': 'string'},
        {'name': 'jurisdiction', 'type': 'string', 'facet': True},
        {'name': 'company_type', 'type': 'string', 'facet': True},
    ]

},
    node_factory.ol_address_str: {
        'name': node_factory.ol_address_str,
        'fields': [
            {'name': 'name', 'type': 'string'},
            {'name': 'address', 'type': 'string'},
            {'name': 'countries', 'type': 'string', 'facet': True},
        ]

    },
    node_factory.ol_officer_str: {
        'name': node_factory.ol_officer_str,
        'fields': [
            {'name': 'name', 'type': 'string'},
            {'name': 'countries', 'type': 'string', 'facet': True},
        ]

    },
    node_factory.ol_intermediary_str: {
        'name': node_factory.ol_intermediary_str,
        'fields': [

            {'name': 'name', 'type': 'string'},
            {'name': 'countries', 'type': 'string', 'facet': True},
        ],

    },
    node_factory.ol_other_str: {
        'name': node_factory.ol_other_str,
        'fields': [

            {'name': 'name', 'type': 'string'},
            {'name': 'type', 'type': 'string', 'facet': True},
        ],

    }}

electoral_commission_schemas ={
    node_factory.ec_regulated_entity_str: {
        'name': node_factory.ec_regulated_entity_str,
        'fields': [{'name': 'name', 'type': 'string', 'facet': False}]

    },
    node_factory.ec_donor_str: {
        'name': node_factory.ec_donor_str,
        'fields': [{'name': 'name', 'type': 'string', 'facet': False}]

    }
}


def connect_to_db(db_name):
    config = helpers.get_config()

    conn = psycopg2.connect(database=db_name,
                            host=config.database_host,
                            user=config.database_user,
                            password=config.database_pw,
                            port=config.database_port)

    return conn


def create_table(db_name, table_name, cols):
    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    cursor.execute(f'drop table if exists {table_name}')

    create_sql = f"""
    CREATE TABLE {table_name}({cols});
    """

    cursor.execute(create_sql)

    conn.commit()
    conn.close()


def render_create_table_instructions(cols):
    text_type = 'text'

    col_instructions = ', '.join([f'{col} {text_type}' for col in cols])
    dtypes = {col: Text() for col in cols}

    return col_instructions, dtypes


def populate_postgres_db(dfs, db_name):
    config = helpers.get_config()
    db = create_engine(
        f'postgresql+psycopg2://postgres:{config.database_pw}@{config.database_host}/{db_name}')
    conn = db.connect()

    for table_name, df in dfs.items():
        print(table_name)
        df = df.fillna(
            psycopg2.extensions.AsIs('NULL'))
        cols = df.columns.to_list()

        col_instructions, dtypes = render_create_table_instructions(cols)

        # create_table(db_name=db_name, table_name=table_name, cols=col_instructions)

        df.to_sql(table_name.lower(), con=conn, if_exists='replace', index=False, dtype=dtypes)


def clear_old_collections(data, client):
    collections = client.collections.retrieve()

    collection_names = [datum['schema']['name'] for datum in data]

    for collection in collections:
        if collection['name'] in collection_names:
            client.collections[collection['name']].delete()


def fetchall_to_nodes(cursor):
    raw_nodes = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    if raw_nodes is None:
        return None

    nodes = []

    for raw_node in raw_nodes:
        node = {}
        for i in range(len(column_names)):
            node[column_names[i]] = raw_node[i]
        nodes.append(node)

    return nodes


def find_new_rows(temp_table_name, table_name, cursor, cols):
    cols = ', '.join(cols)

    query = f"""
    select * from {temp_table_name} except select {cols} from {table_name}
    """

    cursor.execute(query)

    new_donations = fetchall_to_nodes(cursor)

    return cursor, new_donations


def create_temp_table_with_latest_data(cur, table_name, df):
    data_dicts = df.to_dict('records')
    cols = [col for col in data_dicts[0].keys()]

    col_instructions, dtypes = render_create_table_instructions(cols)

    cols_for_insert = ', '.join(cols)

    cur.execute(f'create temp table {table_name} ({col_instructions});')

    query = f"""
        insert into {table_name} ({cols_for_insert}) values %s;
    """

    params = [tuple(datum.values()) for datum in data_dicts]

    execute_values(cur, query, params)

    return cur, cols


def populate_typesense(data):
    client = typesense_client.make_typesense_client()

    clear_old_collections(data, client)

    for datum in data:
        schema = datum['schema']
        client.collections.create(schema)
        typesense_client.import_df(client=client, df=datum['df'], collection=schema['name'])


def update_tables(new_items_dfs, module_database):
    conn = connect_to_db(module_database)
    cursor = conn.cursor()

    for table, df in new_items_dfs.items():

        if len(df) > 0:
            df = df.fillna(
                psycopg2.extensions.AsIs('NULL'))

            values = df.to_dict('records')

            query = f"""
                            insert into {table} values %s;
                        """

            params = [tuple(row.values()) for row in values]

            execute_values(cursor, query, params)


def update_typesense(new_nodes_dfs):
    client = typesense_client.make_typesense_client()

    for collection, df in new_nodes_dfs.items():
        if len(df) > 0:
            typesense_client.import_df(client=client, df=df, collection=collection)


# ---------------------------------------------- ELECTORAL COMMISSION --------------------------------------------

def electoral_commission_find_donations_diffs():
    config = helpers.get_config()
    donations_df = pd.read_csv(config.raw_registered_interests_donations_csv_path)
    donations_df = electoral_commission_prepare_donations_df(donations_df)
    donations_df = donations_df.fillna(
        psycopg2.extensions.AsIs('NULL'))
    conn = connect_to_db(config.roi_database)
    cursor = conn.cursor()

    temp_table_name = 'latest_donations'

    cursor, cols = create_temp_table_with_latest_data(cursor, temp_table_name, donations_df)
    cursor, new_donations = find_new_rows(cursor=cursor, cols=cols, temp_table_name=temp_table_name,
                                          table_name='donations')
    cursor.execute(f'drop table {temp_table_name}')

    conn.commit()
    conn.close()

    return pd.DataFrame(new_donations)

good_count = 0
bad_count = 0

def clean_company_reg_number(reg):

    if pd.isna(reg):
        return reg

    bads = [' ', '(', ')', '-']

    for bad in bads:
        reg = reg.replace(bad, '')

    if len(reg) == 8:
        return reg
    elif len(reg) == 7:
        return '0' + reg
    else:
        return numpy.nan



def electoral_commission_prepare_donations_df(donations_df):
    donations_df = donations_df.dropna(subset=['DonorName', 'DonorId'])
    donations_df.update(donations_df.loc[:, ['DonorName', 'RegulatedEntityName']].apply(
        lambda x: x.str.strip()))

    donations_df['CompanyRegistrationNumber'] = donations_df['CompanyRegistrationNumber'].apply(clean_company_reg_number)

    donations_df['DonorId'] = donations_df['DonorId'].astype(int)

    return donations_df


def electoral_commission_merge_dfs(donations_df, regulated_entities_df, donors_df):
    donations_df = donations_df.merge(regulated_entities_df[['RegulatedEntityId', 'node_id']], on='RegulatedEntityId')

    donations_df.rename(columns={'node_id': 'child_node_id'}, inplace=True)
    regulated_entities_df.rename(columns={'RegulatedEntityName': 'name'}, inplace=True)

    donations_df = donations_df.merge(donors_df[['DonorId', 'node_id']], on='DonorId')

    donations_df.rename(columns={'node_id': 'parent_node_id'}, inplace=True)
    donors_df.rename(columns={'DonorName': 'name'}, inplace=True)

    donations_df.drop(columns=['RegulatedEntityId', 'DonorId'], inplace=True)

    return donations_df, regulated_entities_df, donors_df


# Data set has collisions in DonorId, I've emailed electoral commission to ask about it, in mean time just drop all
# colliding rows
def remove_dupes(donations_df):
    donors_df = donations_df[['DonorId', 'CompanyRegistrationNumber', 'DonorStatus', 'DonorName']]
    donors_df = donors_df.drop_duplicates()
    donor_df_groups = donors_df.groupby('DonorId')

    bad_donor_ids = []

    for group in donor_df_groups:
        if len(group[1]) > 1:
            bad_donor_ids.append(group[1].iloc[0]['DonorId'])

    donations_df = donations_df[~donations_df['DonorId'].isin(bad_donor_ids)]

    return donations_df


def electoral_commission_process_raw_donations_csv():
    config = helpers.get_config()
    donations_df = pd.read_csv(config.raw_registered_interests_donations_csv_path)
    donations_df = electoral_commission_prepare_donations_df(donations_df)
    donations_df = remove_dupes(donations_df)

    regulated_entities_df = donations_df[['RegulatedEntityId', 'RegulatedEntityName', 'RegulatedEntityType'
                                          ]]

    donors_df = donations_df[['DonorId', 'CompanyRegistrationNumber', 'DonorStatus', 'DonorName']]

    regulated_entities_df = regulated_entities_df.drop_duplicates()
    regulated_entities_df['node_id'] = regulated_entities_df.apply(
        lambda row: generate_node_id(row.RegulatedEntityId, node_factory.ec_regulated_entity_str), axis=1)

    donors_df = donors_df.drop_duplicates()
    donors_df['node_id'] = donors_df.apply(
        lambda row: generate_node_id(row.DonorId, node_factory.ec_donor_str), axis=1)

    donations_df, regulated_entities_df, donors_df = electoral_commission_merge_dfs(donations_df,
                                                                                    regulated_entities_df, donors_df)

    nodes_dfs = {node_factory.ec_regulated_entity_str: regulated_entities_df,
                 node_factory.ec_donor_str: donors_df}
    relationships_dfs = {relationship_factory.ec_donation_str: donations_df}

    return nodes_dfs, relationships_dfs


def electoral_commission_find_node_diffs(new_donations_df):
    config = helpers.get_config()
    if len(new_donations_df) == 0:
        return [], []
    conn = connect_to_db(config.roi_database)
    cursor = conn.cursor()

    def get_nodes(table, node_names, node_type):
        query = f'select * from {table} where {table}.name in %s'

        node_tuple = tuple(node_names)

        cursor.execute(query, (node_tuple,))

        all_nodes = fetchall_to_nodes(cursor)
        new_nodes = []
        for node_name in node_names:
            exists = False
            for existing_node in all_nodes:
                if node_name == existing_node['name']:
                    exists = True
                    break
            if not exists:
                new_node = {'name': node_name, 'node_id': generate_node_id(original_node_identifier=node_name,
                                                                           node_type_str=node_type)}
                all_nodes.append(new_node)
                new_nodes.append(new_node)

        return all_nodes, new_nodes

    all_regulated_donees, new_regulated_donees = get_nodes(table=node_factory.ec_regulated_entity_str,
                                                           node_names=new_donations_df['regulated_donee'].unique(),
                                                           node_type=node_factory.ec_regulated_entity_str
                                                           )

    regulated_donees_df = pd.DataFrame(all_regulated_donees)

    all_donors, new_donors = get_nodes(table=node_factory.ec_donor_str,
                                       node_names=new_donations_df['donor'].unique(),
                                       node_type=node_factory.ec_donor_str
                                       )

    donors_df = pd.DataFrame(all_donors)

    donations_df, regulated_donees_df, donors_df = electoral_commission_merge_dfs(new_donations_df,
                                                                                  regulated_donees_df.rename(
                                                                                      columns={
                                                                                          'name': 'regulated_donee'}),
                                                                                  donors_df.rename(
                                                                                      columns={'name': 'donor'}))

    return donations_df, regulated_donees_df, donors_df


def electoral_commission_find_diffs():
    new_donations_without_ids_df = electoral_commission_find_donations_diffs()

    new_donations_df, new_regulated_donees_df, new_donors_df = electoral_commission_find_node_diffs(
        new_donations_without_ids_df)

    print(f'''
        {len(new_donations_df)} new donations
        {len(new_donors_df)} new donors
        {len(new_regulated_donees_df)} new regulated donees
''')

    return {'regulated_donees': new_regulated_donees_df, 'donors': new_donors_df}, \
           {'donations': new_donations_df}


# ---------------------------------------------- ELECTORAL COMMISSION --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- Offshore Leaks --------------------------------------------------
# there are nodes in the intermediaries' dataset with matching node_ids and names to nodes in the officers set. I
# have emailed the ICIJ to let them know and ask what's up. While I wait for this problem to be fixed, going to have
# to just remove the dupe nodes from intermediaries.
def offshore_leaks_remove_dupes_from_intermediaries(node_dfs):
    officer_ids = node_dfs[node_factory.ol_officer_str]['node_id'].tolist()
    intermediaries_df = node_dfs[node_factory.ol_intermediary_str]

    node_dfs[node_factory.ol_intermediary_str] = intermediaries_df[~intermediaries_df['node_id'].isin(officer_ids)]

    return node_dfs


def offshore_leaks_merge_ids(relationships_df, ids_df):
    def merge_part(df, old_col, new_col):
        old_col_df = df[[old_col]]

        old_col_df = pd.merge(
            old_col_df,
            ids_df.rename(columns={'node_id': new_col}),
            left_on=old_col,
            right_index=True,
            how='left',
            sort=False)

        df = pd.concat([df, old_col_df[new_col]], axis=1)

        df.drop([old_col], axis=1, inplace=True)

        return df

    relationships_df = merge_part(relationships_df, 'node_id_start', 'child_node_id')
    relationships_df = merge_part(relationships_df, 'node_id_end', 'parent_node_id')

    return relationships_df


def offshore_leaks_process_raw_csvs():
    config = helpers.get_config()

    relationships_df = pd.read_csv(config.offshore_leaks_directory + '/relationships.csv')
    node_dfs = {node_type: pd.read_csv(f'{config.offshore_leaks_directory}/nodes-{node_type}.csv') for node_type in
                offshore_leaks_node_types}
    node_dfs = offshore_leaks_remove_dupes_from_intermediaries(node_dfs)
    processed_node_dfs = {}

    ids_df = None

    for node_type, node_df in node_dfs.items():
        print(f'{node_type}')
        if len(node_df['node_id'].unique()) != len(node_df):
            print('dupes!')

        node_df.rename(columns={'node_id': 'ol_db_id'}, inplace=True)
        node_df['node_id'] = node_df.apply(lambda row: generate_node_id(row.ol_db_id, node_type), axis=1)
        processed_node_dfs[node_type] = node_df

        if ids_df is None:
            ids_df = node_df[['node_id', 'ol_db_id']]
        else:
            ids_df = pd.concat([ids_df, node_df[['node_id', 'ol_db_id']]], axis=0)

    ids_df.set_index('ol_db_id', inplace=True)

    print('merging ids')
    relationships_df = offshore_leaks_merge_ids(relationships_df, ids_df)

    return processed_node_dfs, {'relationships': relationships_df}


def offshore_leaks_find_diffs():
    config = helpers.get_config()
    node_dfs, relationship_dfs = offshore_leaks_process_raw_csvs()

    dfs = {**node_dfs, **relationship_dfs}

    conn = connect_to_db(config.ol_database)
    cursor = conn.cursor()

    new_rows_dict = {}

    for table_name, df in dfs.items():
        df = df.fillna(
            psycopg2.extensions.AsIs('NULL'))
        temp_table_name = f'latest_{table_name}'
        cursor, cols = create_temp_table_with_latest_data(cursor, temp_table_name, df)
        cursor, new_rows = find_new_rows(cursor=cursor, cols=cols, temp_table_name=temp_table_name,
                                         table_name=table_name)

        if len(new_rows) > 0:
            new_rows_dict[table_name] = pd.DataFrame(new_rows)

        print(f'{len(new_rows)} new {table_name}')

        cursor.execute(f'drop table {temp_table_name}')

    conn.commit()
    conn.close()

    return new_rows_dict


# ---------------------------------------------- Offshore Leaks --------------------------------------------


def full_populate_sequence():
    config = helpers.get_config()

    def each_module(module_specific_processing, module_db, module_schemas):
        print('processing csvs')
        node_dfs, relationship_dfs = module_specific_processing()
        print('populating Postgres')
        populate_postgres_db(db_name=module_db, dfs={**node_dfs, **relationship_dfs})
        data = [{'schema': module_schemas[node_type], 'df': df} for node_type, df in node_dfs.items()]
        print('populating Typesense')
        populate_typesense(data)

    print('Populating DataBases')
    print('Electoral Commission Donations')
    each_module(electoral_commission_process_raw_donations_csv, config.roi_database, electoral_commission_schemas)
    # print('Offshore Leaks')
    # each_module(offshore_leaks_process_raw_csvs, config.ol_database, offshore_leaks_schemas)


def update_sequence():
    config = helpers.get_config()

    def each_module(module_specific_diffs, module_db):
        print('finding diffs')
        new_nodes_dfs, new_relationships_dfs = module_specific_diffs()
        update_tables({**new_nodes_dfs, **new_relationships_dfs}, module_db)
        update_typesense(new_nodes_dfs)

    print('Updating DataBases')
    print('Electoral Commission')
    each_module(electoral_commission_find_diffs, config.roi_database)
    print('Offshore Leaks')
    each_module(offshore_leaks_find_diffs, config.ol_database)
