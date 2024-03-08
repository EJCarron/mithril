from .. import helpers
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from .. import typesense_client
import os
import numpy as np
import glob
import jsonlines
import math


def connect_to_db():
    config = helpers.get_config()

    conn = psycopg2.connect(database=config.roi_database,
                            host=config.database_host,
                            user=config.database_user,
                            password=config.database_pw,
                            port=config.database_port)

    return conn


def create_table(table_name, cols):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute(f'drop table if exists {table_name}')

    create_sql = f"""
    CREATE TABLE {table_name}({cols});
    """

    cursor.execute(create_sql)

    conn.commit()
    conn.close()


def clear_old_collections(ec_collections_names, client):
    collections = client.collections.retrieve()

    for collection in collections:
        if collection['name'] in ec_collections_names:
            client.collections[collection['name']].delete()


def populate_typesense():
    config = helpers.get_config()
    client = typesense_client.make_typesense_client()

    schemas = {'donations': {
        'name': 'donations',
        'fields': [{'name': 'regulated_donee', 'type': 'string', 'facet': True},
                   {'name': 'donor', 'type': 'string', 'facet': True},
                   {'name': 'donation_type', 'type': 'string', 'facet': True},
                   {'name': 'destination', 'type': 'string', 'facet': True},
                   {'name': 'nature_of_donation', 'type': 'string', 'facet': True}
                   ]
    },
        'regulated_donees': {
            'name': 'regulated_donees',
            'fields': [{'name': 'name', 'type': 'string', 'facet': False}]

        },
        'donors': {
            'name': 'donors',
            'fields': [{'name': 'name', 'type': 'string', 'facet': False}]

        }
    }

    clear_old_collections(schemas.keys(), client)

    for collection_name, schema in schemas.items():

        client.collections.create(schema)

        go = True
        counter = 0
        while go:
            file_path = f'{config.ec_jsonl_files}/{collection_name}_{counter}.jsonl'

            if not os.path.exists(file_path):
                go = False
                continue

            with open(file_path) as jsonl_file:
                # todo check response
                response = client.collections[schema['name']].documents.import_(jsonl_file.read().encode('utf-8'))

            counter += 1


def convert_raw_donations_file_into_finished_csvs():
    config = helpers.get_config()
    donations_df = pd.read_csv(config.raw_registered_interests_donations_csv_path)
    col_names = donations_df.columns.to_list()
    name_replace = {key: key.replace(' ', '_').lower() for key in col_names}

    donations_df.rename(columns=name_replace, inplace=True)

    donations_df.fillna(' ', inplace=True)

    regulated_donees = list(donations_df['regulated_donee'].unique())
    donors = list(donations_df['donor'].unique())

    regulated_donees_df = pd.DataFrame(
        [{'regulated_donee': donee, 'node_id': (donee + 'regulated donee').encode().hex()} for donee in
         regulated_donees])

    donors_df = pd.DataFrame([{'donor': str(donor),
                               'node_id': (str(donor) + 'donor').encode().hex()} for donor in donors])

    donations_df = donations_df.merge(regulated_donees_df, on='regulated_donee')

    donations_df.rename(columns={'node_id': 'regulated_donee_node_id'}, inplace=True)
    regulated_donees_df.rename(columns={'regulated_donee': 'name'}, inplace=True)

    donations_df = donations_df.merge(donors_df, on='donor')

    donations_df.rename(columns={'node_id': 'donor_node_id'}, inplace=True)
    donors_df.rename(columns={'donor': 'name'}, inplace=True)

    donations_df.to_csv(f'{config.ec_ready_csv_files}/donations.csv', index=False)
    regulated_donees_df.to_csv(f'{config.ec_ready_csv_files}/regulated_donees.csv', index=False)
    donors_df.to_csv(f'{config.ec_ready_csv_files}/donors.csv', index=False)


def populate_postgres_db():
    config = helpers.get_config()
    db = create_engine(
        f'postgresql+psycopg2://postgres:{config.database_pw}@{config.database_host}/{config.roi_database}')
    conn = db.connect()

    donations_df = pd.read_csv(f'{config.ec_ready_csv_files}/donations.csv')
    regulated_donees_df = pd.read_csv(f'{config.ec_ready_csv_files}/regulated_donees.csv')
    donors_df = pd.read_csv(f'{config.ec_ready_csv_files}/donors.csv')

    def make_table(df, table_name):
        cols = df.columns.to_list()

        col_instructions = ','.join([f'{col} text' for col in cols])

        create_table(table_name, col_instructions)

        df.to_sql(table_name, con=conn, if_exists='replace', index=False)

    make_table(donations_df, 'donations')
    make_table(regulated_donees_df, 'regulated_donees')
    make_table(donors_df, 'donors')


def get_dfs_split_to_size(csv_path):
    file_size = os.path.getsize(csv_path)

    num_splits = math.ceil(file_size / 70000000)

    whole_df = pd.read_csv(csv_path)

    split_dfs = np.array_split(whole_df, num_splits)

    return split_dfs


def clear_jsonl_from_directory(directory_path):
    files = glob.glob(f"{directory_path}/*.jsonl")
    for f in files:
        os.remove(f)


def convert_dfs_to_jsonl(file_name, jsonl_directory_path, dfs):
    for i in range(len(dfs)):
        df = dfs[i]

        dicts = df.to_dict('records')

        new_path = f'{jsonl_directory_path}/{file_name}_{i}.jsonl'

        with jsonlines.open(new_path, 'w') as writer:
            writer.write_all(dicts)


def convert_to_jsonl_split_to_size():
    config = helpers.get_config()

    donations_split_dfs = get_dfs_split_to_size(f'{config.ec_ready_csv_files}/donations.csv')
    regulated_donee_split_dfs = get_dfs_split_to_size(f'{config.ec_ready_csv_files}/regulated_donees.csv')
    donor_split_dfs = get_dfs_split_to_size(f'{config.ec_ready_csv_files}/donors.csv')

    clear_jsonl_from_directory(config.ec_jsonl_files)

    convert_dfs_to_jsonl('donations', config.ec_jsonl_files, donations_split_dfs)
    convert_dfs_to_jsonl('regulated_donees', config.ec_jsonl_files, regulated_donee_split_dfs)
    convert_dfs_to_jsonl('donors', config.ec_jsonl_files, donor_split_dfs)


def full_populate_sequence():
    convert_raw_donations_file_into_finished_csvs()
    populate_postgres_db()
    convert_to_jsonl_split_to_size()
    populate_typesense()
