import os
import toml
import json
import redis
import pymongo
import logging
import psycopg2
import pandas as pd
from dotenv import load_dotenv

from utils.storage import generate_psql_connection_string
from data.models.otodom import OtodomOffer
from exceptions import AlreadyStoredOffer


load_dotenv()

with open("../src/conf/config.toml", "r") as f:
    config = toml.load(f)


class StorageManager:
    def __init__(self, service_name: str, property_type: str,
                 scraper_name: str, mode: int):
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

        self._log = logging.getLogger(scraper_name)

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
        n_success = 0
        table_name = f"{self.service_name.lower()}_{self.property_type.lower()}"
        conn_str = generate_psql_connection_string(**self.postgresql_credentials)

        for offer in scraped_offers:
            offer_df = offer.to_dataframe()
            try:
                offer_df.to_sql(table_name, conn_str,
                                if_exists="append", index=False)
                n_success += 1
            except Exception as e:
                self._log.error(f"Offer {str(offer)} not stored"
                                f" - {str(type(e))}: {str(e)}")

        return n_success

    def get_from_postgresql(self, columns: tuple[str] = ()):
        columns = ", ".join(columns) if columns else "*"
        table_name = f"{self.service_name.lower()}_{self.property_type.lower()}"
        conn_str = generate_psql_connection_string(**self.postgresql_credentials)
        return pd.read_sql(f"SELECT {columns} FROM {table_name}", conn_str)

    def truncate_postgresql_table(self):
        if self.mode == 2:
            self._log.warning("Attempted to truncate on production")
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
        urls_in_db = [doc["url"] for doc in
                      list(self.mongo_collection.find({}, {"url": 1, "_id": 0}))]

        n_success = 0
        for offer in scraped_offers:
            offer_dict = offer.to_dict(parse_json=True)
            try:
                if offer_dict["url"] in urls_in_db:
                    raise AlreadyStoredOffer("Offer already stored in mongo")

                self.mongo_collection.insert_one(offer_dict)
                n_success += 1
            except Exception as e:
                self._log.error(f"Offer {str(offer)} not stored"
                                f" - {str(type(e))}: {str(e)}")

        return n_success

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
            self._log.warning(
                f"Tried to cache data with unsupported type {type(data)}")

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
