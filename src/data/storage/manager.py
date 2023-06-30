import os
import toml
import json
import redis
import pymongo
import psycopg2
import pandas as pd
from dotenv import load_dotenv

from utils.storage import generate_psql_connection_string
from data.models.otodom import OtodomOffer


load_dotenv()

with open("../src/conf/config.toml", "r") as f:
    config = toml.load(f)


class StorageManager:
    def __init__(self, service_name: str, property_type: str, mode: int):
        """
        Create an instance of a StorageManager for a given service name
        and property type

        Modes:
        0 - test
        1 - dev
        2 - prod
        """
        self.service_name: str = service_name.upper()
        self.property_type: str = property_type.upper()
        self.mode: int = mode

        self.postgresql_credentials = self._configure_postgresql()
        self.mongo_collection = self._configure_mongodb()
        # self.bq_config = self._configure_big_query()
        self.redis_db = self._configure_redis()

    def _configure_postgresql(self):
        psql_credentials = {
            "user": os.getenv("POSTGRESQL_USER"),
            "password": os.getenv("POSTGRESQL_PASSWORD"),
            "host": os.getenv("POSTGRESQL_HOST"),
            "port": os.getenv("POSTGRESQL_PORT"),
            "dbname": list(config["postgresql"].values())[self.mode]
        }
        return psql_credentials

    def _configure_mongodb(self):
        mongo_db_name = list(config["mongodb"].values())[self.mode]
        mongo_collection_name = f"{self.service_name.lower()}_{self.property_type.lower()}"
        mongo_client = pymongo.MongoClient()
        mongo_db = mongo_client[mongo_db_name]
        mongo_collection = mongo_db[mongo_collection_name]
        return mongo_collection

    def _configure_redis(self):
        host, port, *databases = config["redis"].values()
        return redis.Redis(host=host, port=port, db=databases[self.mode])

    def store_in_postgresql(self, scraped_offers: list[OtodomOffer]):
        table_name = f"{self.service_name.lower()}_{self.property_type.lower()}"
        conn_str = generate_psql_connection_string(**self.postgresql_credentials)

        for offer in scraped_offers:
            offer = offer.to_dataframe()
            offer.to_sql(table_name, conn_str, if_exists="append", index=False)

    def get_from_postgresql(self):
        table_name = f"{self.service_name.lower()}_{self.property_type.lower()}"
        conn_str = generate_psql_connection_string(**self.postgresql_credentials)
        return pd.read_sql(f"SELECT * FROM {table_name}", conn_str)

    def truncate_postgresql_table(self):
        if self.mode == 2:
            # TODO warning - truncate on production
            return

        if self.mode == 1:
            x = input("Sure to truncate?: [y/n]")
            if x != "y":
                return

        table_name = f"{self.service_name.lower()}_{self.property_type.lower()}"
        conn = psycopg2.connect(**self.postgresql_credentials)
        cursor = conn.cursor()
        cursor.execute(f"TRUNCATE TABLE {table_name}")
        conn.commit()
        cursor.close()
        conn.close()

    def store_in_mongodb(self, scraped_offers: list[OtodomOffer]):
        for offer in scraped_offers:
            offer = offer.to_dict(parse_json=True)
            self.mongo_collection.insert_one(offer)

    def get_from_mongodb(self):
        return self.mongo_collection.find({}, {"_id": 0})

    def truncate_mongodb_collection(self):
        self.mongo_collection.drop()

    def store_in_bigquery(self, scraped_offers):
        pass

    def cache_data(self, key: str, data: str | list[str]):
        """
        Puts data to cache under the given key.
        If list, dict or tuple, first json.dumps() it
        """
        if isinstance(data, (str, int, float)):
            self.redis_db.set(key, data)
        elif isinstance(data, (list, dict, tuple)):
            self.redis_db.set(key, json.dumps(data))
        else:
            # TODO: warning
            pass

    def read_cache(self, key: str, from_json: bool = False):
        """
        Reads from cache under a given key and returns the value.
        If `from_json` then it json.loads() first.
        """
        value = self.redis_db.get(key)
        if from_json:
            return json.loads(value)
        else:
            return value

    def clear_cache(self, key: str) -> int:
        """
        Clears cache under a given key and returns if success
        """
        return self.redis_db.delete(key)
