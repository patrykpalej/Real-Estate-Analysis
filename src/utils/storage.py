import os
import toml
import pandas as pd
from dotenv import load_dotenv


def generate_psql_connection_string(user, password, host, port, dbname):
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def get_credentials():
    load_dotenv()
    user = os.environ["POSTGRESQL_USER_VPS"]
    password = os.environ["POSTGRESQL_PASSWORD_VPS"]
    host = os.environ["POSTGRESQL_HOST_VPS"]
    port = os.environ["POSTGRESQL_PORT_VPS"]

    with open("../src/conf/config.toml", "r") as f:
        toml_config = toml.load(f)
    dbname = toml_config["postgresql"]["db_prod"]

    return user, password, host, port, dbname


def read_from_db(sql, conn_str):
    df = pd.read_sql(sql, conn_str)
    return df
