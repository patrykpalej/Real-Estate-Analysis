# import os
# import toml
# from scraping.logger import setup_logger
#
#
# with open("../src/conf/config.toml", "r") as f:
#     config_toml = toml.load(f)
#
#
# # Scraping logger
# def get_logger(name: str):
#     return setup_logger(name,
#                         int(os.environ.get("loglevel", 10)),
#                         to_file=config_toml["logging"]["to_file"],
#                         to_stdout=config_toml["logging"]["to_stdout"])
