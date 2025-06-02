import os
import logging
import sys


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


def create_logger():
    logger = logging.getLogger('interwebs_speed')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('interwebs_speed.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger


def get_config() -> dict:
    return {
        'csv_files_path': os.getenv('CSV_FILES_PATH'),
        'internet_speed': float(os.getenv('INTERNET_SPEED')),
        'expected_download': float(os.getenv('EXPECTED_DOWNLOAD')),
        'expected_upload': float(os.getenv('EXPECTED_UPLOAD')),
        'smtp_host': os.getenv('SMTP_HOST'),
        'smtp_port': int(os.getenv('SMTP_PORT')),
        'smtp_username': os.getenv('SMTP_USERNAME'),
        'smtp_password': os.getenv('SMTP_PASSWORD'),
        'alert_sender_mail': os.getenv('ALERT_SENDER_MAIL'),
        'alert_receiver_mail': os.getenv('ALERT_RECEIVER_MAIL')
    }


def format_csv_line(*args):
    return ','.join(map(str, args))


def mb_to_bytes(n: float) -> float:
    return n * 1000000


def bytes_to_mb(n: float) -> float:
    return n / 1000000
