import json
import random
from datetime import datetime


PATH_TO_HEADERS_CONFIG = "conf/scraping/headers.json"


def generate_random_headers():
    with open(PATH_TO_HEADERS_CONFIG, "r") as file:
        headers_config = json.load(file)

    headers_names = headers_config.keys()
    random_headers = dict().fromkeys(headers_names)
    for key in headers_names:
        random_headers[key] = random.choice(headers_config[key])

    return random_headers


def generate_scraper_name(service_name: str, property_type: str) -> str:
    return (datetime.now().strftime("%y%m%d-%H%M")
            + "_" + service_name
            + "_" + property_type)


if __name__ == "__main__":
    pass
