import json
import random


PATH_TO_HEADERS_CONFIG = "conf/requesting/headers.json"


def generate_random_headers():
    with open(PATH_TO_HEADERS_CONFIG, "r") as file:
        headers_config = json.load(file)

    headers_names = headers_config.keys()
    random_headers = dict().fromkeys(headers_names)
    for key in headers_names:
        random_headers[key] = random.choice(headers_config[key])

    return random_headers


if __name__ == "__main__":
    headers = generate_random_headers()
    print(headers)
