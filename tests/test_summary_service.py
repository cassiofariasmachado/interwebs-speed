import pytest
from unittest.mock import patch, MagicMock
from interwebs_speed.services.summary_service import send_monthly_summary

@pytest.fixture
def mocks():
    with patch('interwebs_speed.services.summary_service.get_config') as mock_get_config, \
            patch('interwebs_speed.services.summary_service.create_logger') as mock_create_logger, \
            patch('interwebs_speed.services.summary_service.mail_service') as mock_mail_service, \
            patch('os.path.exists') as mock_path_exists, \
            patch('interwebs_speed.services.summary_service._load_data') as mock_load_data, \
            patch('interwebs_speed.services.summary_service._get_summary') as mock_get_summary, \
            patch('interwebs_speed.services.summary_service._to_html') as mock_to_html:

        mock_get_config.return_value = {
            'csv_files_path': '/tmp',
        }
        mock_logger = MagicMock()
        mock_create_logger.return_value = mock_logger

        yield {
            'mock_get_config': mock_get_config,
            'mock_create_logger': mock_create_logger,
            'mock_logger': mock_logger,
            'mock_mail_service': mock_mail_service,
            'mock_path_exists': mock_path_exists,
            'mock_load_data': mock_load_data,
            'mock_get_summary': mock_get_summary,
            'mock_to_html': mock_to_html,
        }

def test_send_monthly_summary_success(mocks):
    mocks['mock_path_exists'].return_value = True
    mocks['mock_load_data'].return_value = [{'download': 100, 'upload': 50, 'ping': 10}]
    mocks['mock_get_summary'].return_value = {'avg_download': 100, 'avg_upload': 50, 'avg_ping': 10}
    mocks['mock_to_html'].return_value = '<html></html>'

    send_monthly_summary()

    mocks['mock_logger'].info.assert_any_call('Starting monthly summary.')
    mocks['mock_mail_service'].send_email.assert_called_once_with(
        mocks['mock_get_config'].return_value,
        "Internet Speed Monthly Summary",
        '<html></html>',
        subtype="html"
    )
    mocks['mock_logger'].info.assert_any_call('Monthly summary sent.')

def test_send_monthly_summary_file_not_found(mocks):
    mocks['mock_path_exists'].return_value = False

    send_monthly_summary()

    mocks['mock_logger'].error.assert_called_once()
    mocks['mock_mail_service'].send_email.assert_not_called()
