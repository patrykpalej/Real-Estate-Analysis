import logging


def setup_logger(name: str, level: int,
                 to_file: bool = True, to_stdout: bool = True):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
        "%Y-%m-%d %H:%M:%S")

    if to_file:
        file_handler = logging.FileHandler(f"../src/scraping/logs/{name}.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if to_stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
