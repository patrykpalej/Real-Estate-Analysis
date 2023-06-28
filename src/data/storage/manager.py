import os
import toml
import json
import redis
import pymongo

from utils.storage import generate_psql_connection_string
from data.models.otodom import OtodomOffer


toml_config = toml.load("../src/conf/config.toml")


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
        self.service_name = service_name
        self.property_type = property_type
        self.mode = mode

        host, port, *databases = toml_config["redis"].values()
        self.redis_db = redis.Redis(host=host, port=port, db=databases[mode])

    def store_in_postgresql(self, scraped_offers: list[OtodomOffer]):
        db_user = os.getenv("POSTGRESQL_USER")
        db_password = os.getenv("POSTGRESQL_PASSWORD")
        db_host = os.getenv("POSTGRESQL_HOST")
        db_port = os.getenv("POSTGRESQL_PORT")
        db_name = list(toml_config["postgresql"].values())[self.mode]

        table_name = f"{self.service_name.lower()}_{self.property_type.lower()}"

        conn_str = generate_psql_connection_string(db_user,
                                                   db_password,
                                                   db_host,
                                                   db_port,
                                                   db_name)

        for offer in scraped_offers:
            offer = offer.to_dataframe()
            offer.to_sql(table_name, conn_str, if_exists="append", index=False)

    def store_in_mongodb(self, scraped_offers: list[OtodomOffer]):
        db_name = list(toml_config["postgresql"].values())[self.mode]
        collection_name = f"{self.service_name.lower()}_{self.property_type.lower()}"

        client = pymongo.MongoClient()
        db = client[db_name]
        collection = db[collection_name]

        for offer in scraped_offers:
            offer = offer.to_dict(parse_json=True)
            collection.insert_one(offer)

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
