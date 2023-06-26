from datetime import datetime


def generate_scraper_name(service_name: str, property_type: str) -> str:
    return (datetime.now().strftime("%y%m%d-%H%M")
            + "_" + service_name
            + "_" + property_type)
