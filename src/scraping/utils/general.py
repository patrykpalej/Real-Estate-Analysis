from datetime import datetime


def generate_scraper_name(property_type):
    return datetime.now().strftime("%y%m%d-%H%M") + "_" + property_type
