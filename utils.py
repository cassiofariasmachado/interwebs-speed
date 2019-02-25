import os
import logging


from services import file_service


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def create_logger():
    logger = logging.getLogger('interwebs_speed')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('interwebs_speed.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger


def get_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    return file_service.load_config(config_path)


def format_csv_line(*args):
    return ','.join(map(str, args))