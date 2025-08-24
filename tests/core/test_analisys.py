import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from interwebs_speed.core.analisys import Analysis
from interwebs_speed.utils import bytes_to_mb

@pytest.fixture
def mock_datetime():
    with patch('interwebs_speed.core.analisys.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2023, 10, 26, 12, 0, 0)
        yield mock_dt

@pytest.fixture
def analysis_instance(mock_datetime):
    return Analysis(download=80.0, upload=8.0, ping=5.0)

def test_analysis_init(analysis_instance, mock_datetime):
    assert analysis_instance.download == 80.0
    assert analysis_instance.upload == 8.0
    assert analysis_instance.ping == 5.0
    assert analysis_instance.date == mock_datetime.now.return_value

def test_is_under_expected_true(analysis_instance):
    # Assuming expected_download and expected_upload are also in bytes for comparison
    assert analysis_instance.is_under_expected(expected_download=90.0, expected_upload=10.0) is True

def test_is_under_expected_false(analysis_instance):
    assert analysis_instance.is_under_expected(expected_download=70.0, expected_upload=5.0) is False

def test_download_is_under_expected_true(analysis_instance):
    assert analysis_instance.download_is_under_expected(expected_download=90.0) is True

def test_download_is_under_expected_false(analysis_instance):
    assert analysis_instance.download_is_under_expected(expected_download=70.0) is False

def test_upload_is_under_expected_true(analysis_instance):
    assert analysis_instance.upload_is_under_expected(expected_upload=10.0) is True

def test_upload_is_under_expected_false(analysis_instance):
    assert analysis_instance.upload_is_under_expected(expected_upload=5.0) is False

@patch('interwebs_speed.core.analisys.bytes_to_mb')
def test_mount_analysis_mail_both_under(mock_bytes_to_mb, analysis_instance):
    mock_bytes_to_mb.side_effect = lambda x: f"{x / 1000000:.2f}"
    expected_download = 90.0
    expected_upload = 10.0
    message = analysis_instance.mount_analysis_mail(expected_download, expected_upload)
    assert "Download is under expected, please check it." in message
    assert "Upload is under expected, please check it." in message
    assert "- Download: 0.00 MB" in message
    assert "- Upload: 0.00 MB" in message
    assert "- Ping: 5.0 ms" in message

@patch('interwebs_speed.core.analisys.bytes_to_mb')
def test_mount_analysis_mail_download_under(mock_bytes_to_mb, analysis_instance):
    mock_bytes_to_mb.side_effect = lambda x: f"{x / 1000000:.2f}"
    expected_download = 90.0
    expected_upload = 5.0 # Upload is not under expected
    message = analysis_instance.mount_analysis_mail(expected_download, expected_upload)
    assert "Download is under expected, please check it." in message
    assert "Upload is under expected, please check it." not in message
    assert "- Download: 0.00 MB" in message
    assert "- Upload: 0.00 MB" in message
    assert "- Ping: 5.0 ms" in message

@patch('interwebs_speed.core.analisys.bytes_to_mb')
def test_mount_analysis_mail_upload_under(mock_bytes_to_mb, analysis_instance):
    mock_bytes_to_mb.side_effect = lambda x: f"{x / 1000000:.2f}"
    expected_download = 70.0 # Download is not under expected
    expected_upload = 10.0
    message = analysis_instance.mount_analysis_mail(expected_download, expected_upload)
    assert "Download is under expected, please check it." not in message
    assert "Upload is under expected, please check it." in message
    assert "- Download: 0.00 MB" in message
    assert "- Upload: 0.00 MB" in message
    assert "- Ping: 5.0 ms" in message

@patch('interwebs_speed.core.analisys.bytes_to_mb')
def test_mount_analysis_mail_normal(mock_bytes_to_mb, analysis_instance):
    mock_bytes_to_mb.side_effect = lambda x: f"{x / 1000000:.2f}"
    expected_download = 70.0 # Download is not under expected
    expected_upload = 5.0 # Upload is not under expected
    message = analysis_instance.mount_analysis_mail(expected_download, expected_upload)
    assert "Download is under expected, please check it." not in message
    assert "Upload is under expected, please check it." not in message
    assert "- Download: 0.00 MB" in message
    assert "- Upload: 0.00 MB" in message
    assert "- Ping: 5.0 ms" in message
