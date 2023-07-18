import toml
import logging


with open("../src/conf/config.toml", "r") as f:
    config = toml.load(f)["logging"]


def setup_logger(name: str,
                 to_file: bool = True, to_stdout: bool = True):
    logger = logging.getLogger(name)
    logger.setLevel(config["default_log_level"])

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
        "%Y-%m-%d %H:%M:%S")

    if to_file:
        file_handler = logging.FileHandler(f"../src/scraping/logs/{name}.log")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(config["file_log_level"])
        logger.addHandler(file_handler)

    if to_stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(config["stdout_log_level"])
        logger.addHandler(stream_handler)

    return logger
