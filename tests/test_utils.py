import pytest
from interwebs_speed.utils import get_config


@pytest.fixture
def env_vars(monkeypatch):
    monkeypatch.setenv('CSV_FILES_PATH', '/tmp/csvs')
    monkeypatch.setenv('INTERNET_SPEED', '100.5')
    monkeypatch.setenv('EXPECTED_DOWNLOAD', '90.0')
    monkeypatch.setenv('EXPECTED_UPLOAD', '10.0')
    monkeypatch.setenv('SMTP_HOST', 'smtp.example.com')
    monkeypatch.setenv('SMTP_PORT', '587')
    monkeypatch.setenv('SMTP_USERNAME', 'user')
    monkeypatch.setenv('SMTP_PASSWORD', 'pass')
    monkeypatch.setenv('ALERT_SENDER_MAIL', 'sender@example.com')
    monkeypatch.setenv('ALERT_RECEIVER_MAIL', 'receiver@example.com')


def test_get_config(env_vars):
    config = get_config()

    assert config['csv_files_path'] == '/tmp/csvs'
    assert config['internet_speed'] == 100.5
    assert config['expected_download'] == 90.0
    assert config['expected_upload'] == 10.0
    assert config['smtp_host'] == 'smtp.example.com'
    assert config['smtp_port'] == 587
    assert config['smtp_username'] == 'user'
    assert config['smtp_password'] == 'pass'
    assert config['alert_sender_mail'] == 'sender@example.com'
    assert config['alert_receiver_mail'] == 'receiver@example.com'


def test_get_config_missing_env(env_vars, monkeypatch):
    monkeypatch.delenv('CSV_FILES_PATH', raising=False)

    config = get_config()

    assert config['csv_files_path'] is None
