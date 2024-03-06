from .. import helpers
import pandas as pd
from sqlalchemy import create_engine
import psycopg2


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


def populate_db():
    config = helpers.get_config()
    db = create_engine(f'postgresql+psycopg2://postgres:{config.database_pw}@{config.database_host}/{config.roi_database}')
    conn = db.connect()

    donations_df = pd.read_csv(config.registered_interests_donations_csv_path)
    col_names = donations_df.columns.to_list()
    name_replace = {key: key.replace(' ', '_') for key in col_names}

    donations_df.rename(columns=name_replace, inplace=True)

    regulated_donees = list(donations_df['Regulated_Donee'].unique())
    donors = list(donations_df['Donor'].unique())

    regulated_donees_df = pd.DataFrame(
        [{'name': donee, 'node_id': (donee + 'regulated donee').encode().hex()} for donee in
         regulated_donees])

    donors_df = pd.DataFrame([{'name': str(donor),
                               'node_id': (str(donor) + 'donor').encode().hex()} for donor in donors])

    def make_table(df, table_name):

        cols = df.columns.to_list()

        col_instructions = ','.join([f'{col} text' for col in cols])

        create_table(table_name, col_instructions)

        df.to_sql(table_name, con=conn, if_exists='replace', index=False)

    make_table(donations_df, 'donations')
    make_table(regulated_donees_df, 'regulated_donees')
    make_table(donors_df, 'donors')





