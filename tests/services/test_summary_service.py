import pytest
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta
import csv
import os

from interwebs_speed.services.summary_service import send_monthly_summary, _load_data, _get_summary, _to_html, _get_data_summary
from interwebs_speed.core.analisys import Analysis # Although not directly used, it's good practice to import if related

@pytest.fixture
def mock_config():
    return {
        'csv_files_path': '/tmp',
    }

@pytest.fixture
def mocks(mock_config):
    with patch('interwebs_speed.services.summary_service.get_config', return_value=mock_config), \
            patch('interwebs_speed.services.summary_service.create_logger') as mock_create_logger, \
            patch('interwebs_speed.services.summary_service.mail_service') as mock_mail_service, \
            patch('os.path.exists') as mock_path_exists, \
            patch('interwebs_speed.services.summary_service._load_data') as mock_load_data, \
            patch('interwebs_speed.services.summary_service._get_summary') as mock_get_summary, \
            patch('interwebs_speed.services.summary_service._to_html') as mock_to_html:

        mock_logger = MagicMock()
        mock_create_logger.return_value = mock_logger

        yield {
            'mock_config': mock_config,
            'mock_create_logger': mock_create_logger,
            'mock_logger': mock_logger,
            'mock_mail_service': mock_mail_service,
            'mock_path_exists': mock_path_exists,
            'mock_load_data': mock_load_data,
            'mock_get_summary': mock_get_summary,
            'mock_to_html': mock_to_html,
        }

# Tests for send_monthly_summary
def test_send_monthly_summary_current_month_success(mocks):
    mocks['mock_path_exists'].return_value = True
    mocks['mock_load_data'].return_value = [{'download': 100, 'upload': 50, 'ping': 10}]
    mocks['mock_get_summary'].return_value = {'avg_download': 100, 'avg_upload': 50, 'avg_ping': 10}
    mocks['mock_to_html'].return_value = '<html></html>'

    # Mock datetime.now to ensure consistent file naming
    with patch('interwebs_speed.services.summary_service.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2023, 10, 26)
        send_monthly_summary(previous_month=False)

    date = datetime(2023, 10, 26)
    subject = f"Internet Speed Monthly Summary - {date.strftime('%m-%Y')}"

    mocks['mock_logger'].info.assert_any_call('Starting monthly summary.')
    mocks['mock_mail_service'].send_email.assert_called_once_with(
        mocks['mock_config'],
        subject,
        '<html></html>',
        subtype="html"
    )
    mocks['mock_logger'].info.assert_any_call('Monthly summary sent.')

def test_send_monthly_summary_previous_month_success(mocks):
    mocks['mock_path_exists'].return_value = True
    mocks['mock_load_data'].return_value = [{'download': 100, 'upload': 50, 'ping': 10}]
    mocks['mock_get_summary'].return_value = {'avg_download': 100, 'avg_upload': 50, 'avg_ping': 10}
    mocks['mock_to_html'].return_value = '<html></html>'

    # Mock datetime.now to ensure consistent file naming
    with patch('interwebs_speed.services.summary_service.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2023, 10, 26)
        send_monthly_summary(previous_month=True)

    today = datetime(2023, 10, 26)
    first_day_of_current_month = today.replace(day=1)
    date = first_day_of_current_month - timedelta(days=1)
    subject = f"Internet Speed Monthly Summary - {date.strftime('%m-%Y')}"

    mocks['mock_logger'].info.assert_any_call('Starting monthly summary.')
    mocks['mock_mail_service'].send_email.assert_called_once_with(
        mocks['mock_config'],
        subject,
        '<html></html>',
        subtype="html"
    )
    mocks['mock_logger'].info.assert_any_call('Monthly summary sent.')

def test_send_monthly_summary_file_not_found(mocks):
    mocks['mock_path_exists'].return_value = False

    # Mock datetime.now to ensure consistent file naming
    with patch('interwebs_speed.services.summary_service.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2023, 10, 26)
        send_monthly_summary()

    mocks['mock_logger'].error.assert_called_once()
    mocks['mock_mail_service'].send_email.assert_not_called()

# Tests for _load_data
@patch('interwebs_speed.services.summary_service.csv.DictReader')
@patch('builtins.open', new_callable=mock_open)
def test_load_data_success(mock_open_file, mock_dict_reader, mocks):
    mock_dict_reader.return_value = [
        {'download': '100', 'upload': '50', 'ping': '10', 'date': '2023-10-26'},
        {'download': '200', 'upload': '60', 'ping': '12', 'date': '2023-10-27'}
    ]
    file_path = "/tmp/10-2023.csv"
    data = _load_data(file_path)
    mock_open_file.assert_called_once_with(file_path, 'r')
    mock_dict_reader.assert_called_once_with(mock_open_file())
    assert len(data) == 2
    assert data[0]['download'] == pytest.approx(100.0)
    assert data[1]['upload'] == pytest.approx(60.0)

@patch('builtins.open', side_effect=FileNotFoundError)
def test_load_data_file_not_found(mock_file, mocks):
    file_path = "/tmp/non_existent.csv"
    with pytest.raises(FileNotFoundError):
        _load_data(file_path)

# Tests for _get_summary
def test_get_summary_empty_data():
    summary = _get_summary([])
    assert summary == {
        "avg_download": 0, "avg_upload": 0, "avg_ping": 0,
        "min_download": 0, "min_upload": 0, "min_ping": 0,
        "max_download": 0, "max_upload": 0, "max_ping": 0,
    }

def test_get_summary_with_data():
    data = [
        {'download': 100, 'upload': 50, 'ping': 10},
        {'download': 200, 'upload': 60, 'ping': 12},
        {'download': 150, 'upload': 55, 'ping': 11}
    ]
    summary = _get_summary(data)
    assert summary["avg_download"] == pytest.approx(150.0)
    assert summary["avg_upload"] == pytest.approx(55.0)
    assert summary["avg_ping"] == pytest.approx(11.0)
    assert summary["min_download"] == pytest.approx(100.0)
    assert summary["max_upload"] == pytest.approx(60.0)
    assert summary["max_ping"] == pytest.approx(12.0)

# Tests for _to_html
@patch('interwebs_speed.services.summary_service.bytes_to_mb')
def test_to_html(mock_bytes_to_mb):
    mock_bytes_to_mb.side_effect = lambda x: x # bytes_to_mb returns a float, _to_html formats it
    summary_data = {
        "avg_download": 150.0, "avg_upload": 55.0, "avg_ping": 11.0,
        "min_download": 100.0, "min_upload": 50.0, "min_ping": 10.0,
        "max_download": 200.0, "max_upload": 60.0, "max_ping": 12.0,
    }
    html = _to_html(summary_data)
    # Remove all whitespace for robust comparison
    html_stripped = "".join(html.split())

    assert "<h2>InternetSpeedMonthlySummary</h2>" in html_stripped
    assert "<td>Download(MB)</td><td>150.00</td><td>100.00</td><td>200.00</td>" in html_stripped
    assert "<td>Upload(MB)</td><td>55.00</td><td>50.00</td><td>60.00</td>" in html_stripped
    assert "<td>Ping(ms)</td><td>11.00</td><td>10.00</td><td>12.00</td>" in html_stripped

# Tests for _get_data_summary
def test_get_data_summary_current_month():
    with patch('interwebs_speed.services.summary_service.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2023, 10, 26)
        result = _get_data_summary(previous_month=False)
        assert result == datetime(2023, 10, 26)

def test_get_data_summary_previous_month():
    with patch('interwebs_speed.services.summary_service.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2023, 10, 26)
        result = _get_data_summary(previous_month=True)
        assert result == datetime(2023, 9, 30) # Last day of previous month

def test_get_data_summary_previous_month_edge_case():
    with patch('interwebs_speed.services.summary_service.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2023, 1, 15) # January 15th
        result = _get_data_summary(previous_month=True)
        assert result == datetime(2022, 12, 31) # Last day of December of previous year
