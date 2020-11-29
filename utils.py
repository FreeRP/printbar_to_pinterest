import json
import logging


def get_logger(log_file, name):
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s -%(module)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    return logger

def load_json(file):
    with open(file) as json_file:
        return json.load(json_file)
