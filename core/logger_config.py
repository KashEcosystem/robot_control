import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok = True)

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

def setup_logger():   
    logger=logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG) 

    if logger.handlers:
        return logger
    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(f"{LOG_DIR}/robot.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(f"{LOG_DIR}/error.log", encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    return logger
logger = setup_logger()

    