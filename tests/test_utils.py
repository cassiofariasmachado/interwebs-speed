import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

from interwebs_speed.utils import create_logger, get_config, format_csv_line, mb_to_bytes, bytes_to_mb

@patch('interwebs_speed.utils.logging.getLogger')
@patch('interwebs_speed.utils.logging.FileHandler')
@patch('interwebs_speed.utils.logging.StreamHandler')
def test_create_logger(mock_stream_handler, mock_file_handler, mock_get_logger):
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger
    mock_file_handler_instance = MagicMock()
    mock_stream_handler_instance = MagicMock()
    mock_file_handler.return_value = mock_file_handler_instance
    mock_stream_handler.return_value = mock_stream_handler_instance

    logger = create_logger()

    mock_get_logger.assert_called_once_with('interwebs_speed')
    mock_logger.setLevel.assert_called_once_with(logging.DEBUG)
    mock_file_handler.assert_called_once_with('interwebs_speed.log')
    mock_file_handler_instance.setLevel.assert_called_once_with(logging.DEBUG)
    mock_file_handler_instance.setFormatter.assert_called_once()
    mock_stream_handler.assert_called_once_with(sys.stdout)
    mock_stream_handler_instance.setLevel.assert_called_once_with(logging.DEBUG)
    mock_stream_handler_instance.setFormatter.assert_called_once()
    mock_logger.addHandler.assert_any_call(mock_file_handler_instance)
    mock_logger.addHandler.assert_any_call(mock_stream_handler_instance)
    assert logger == mock_logger

@patch('os.getenv')
def test_get_config(mock_getenv):
    mock_getenv.side_effect = lambda key, default=None: {
        'CSV_FILES_PATH': '/tmp',
        'INTERNET_SPEED': '100000000',
        'EXPECTED_DOWNLOAD': '90000000',
        'EXPECTED_UPLOAD': '10000000',
        'SMTP_HOST': 'smtp.example.com',
        'SMTP_PORT': '465',
        'SMTP_USERNAME': 'user@example.com',
        'SMTP_PASSWORD': 'password',
        'ALERT_SENDER_MAIL': 'sender@example.com',
        'ALERT_RECEIVER_MAIL': 'receiver@example.com'
    }.get(key, default)

    config = get_config()

    assert config == {
        'csv_files_path': '/tmp',
        'internet_speed': 100000000.0,
        'expected_download': 90000000.0,
        'expected_upload': 10000000.0,
        'smtp_host': 'smtp.example.com',
        'smtp_port': 465,
        'smtp_username': 'user@example.com',
        'smtp_password': 'password',
        'alert_sender_mail': 'sender@example.com',
        'alert_receiver_mail': 'receiver@example.com'
    }

def test_format_csv_line():
    assert format_csv_line('a', 'b', 'c') == 'a,b,c'
    assert format_csv_line(1, 2, 3) == '1,2,3'
    assert format_csv_line('a', 1, 'c') == 'a,1,c'
    assert format_csv_line() == ''

def test_mb_to_bytes():
    assert mb_to_bytes(1) == 1000000
    assert mb_to_bytes(1.5) == 1500000
    assert mb_to_bytes(0) == 0

def test_bytes_to_mb():
    assert bytes_to_mb(1000000) == 1
    assert bytes_to_mb(1500000) == 1.5
    assert bytes_to_mb(0) == 0
