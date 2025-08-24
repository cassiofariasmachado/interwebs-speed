import pytest
from unittest.mock import patch, MagicMock
from interwebs_speed.services.analisys_service import analyze


@pytest.fixture
def mocks():
    with patch('interwebs_speed.services.analisys_service.get_config') as mock_get_config, \
            patch('interwebs_speed.services.analisys_service.create_logger') as mock_create_logger, \
            patch('interwebs_speed.services.analisys_service.internet_speed_service') as mock_internet_speed_service, \
            patch('interwebs_speed.services.analisys_service.file_service') as mock_file_service, \
            patch('interwebs_speed.services.analisys_service.mail_service') as mock_mail_service, \
            patch('interwebs_speed.services.analisys_service.format_csv_line') as mock_format_csv_line:

        mock_get_config.return_value = {
            'csv_files_path': '/tmp',
            'expected_download': 90.0,
            'expected_upload': 10.0
        }
        mock_logger = MagicMock()
        mock_create_logger.return_value = mock_logger

        mock_analysis = MagicMock()
        mock_analysis.download = 80.0
        mock_analysis.upload = 8.0
        mock_analysis.ping = 5.0
        mock_analysis.date.strftime.return_value = '06-2024.csv'
        mock_internet_speed_service.get_internet_speed.return_value = mock_analysis

        mock_file_service.exists.return_value = False
        mock_format_csv_line.side_effect = lambda *args: ','.join(
            map(str, args))

        yield {
            'mock_get_config': mock_get_config,
            'mock_create_logger': mock_create_logger,
            'mock_logger': mock_logger,
            'mock_internet_speed_service': mock_internet_speed_service,
            'mock_file_service': mock_file_service,
            'mock_mail_service': mock_mail_service,
            'mock_format_csv_line': mock_format_csv_line,
            'mock_analysis': mock_analysis,
        }


def test_analyze_under_expected(mocks):

    mocks['mock_analysis'].is_under_expected.return_value = True
    mocks['mock_analysis'].mount_analysis_mail.return_value = 'alert message'

    analyze()

    mocks['mock_logger'].info.assert_any_call('Starting analyze')
    mocks['mock_logger'].info.assert_any_call(
        'Download or upload is under expected.')
    mocks['mock_mail_service'].send_email.assert_called_once()
    mocks['mock_file_service'].save_csv.assert_called_once()

    args, _kwargs = mocks['mock_file_service'].save_csv.call_args
    assert 'download,upload,ping,date' in args[1][0]


def test_analyze_normal(mocks):
    mocks['mock_analysis'].is_under_expected.return_value = False
    mocks['mock_file_service'].exists.return_value = False

    analyze()

    mocks['mock_logger'].info.assert_any_call(
        'Download and upload are normal.')
    mocks['mock_mail_service'].send_email.assert_not_called()
    mocks['mock_file_service'].save_csv.assert_called_once()

    args, _kwargs = mocks['mock_file_service'].save_csv.call_args

    assert 'download,upload,ping,date' == args[1][0]
    assert 2 == len(args[1])


def test_analyze_file_exists(mocks):
    mocks['mock_analysis'].is_under_expected.return_value = False
    mocks['mock_file_service'].exists.return_value = True

    analyze()

    mocks['mock_logger'].info.assert_any_call(
        'Download and upload are normal.')
    mocks['mock_mail_service'].send_email.assert_not_called()
    mocks['mock_file_service'].save_csv.assert_called_once()

    args, _kwargs = mocks['mock_file_service'].save_csv.call_args

    assert 'download,upload,ping,date' not in args[1]
    assert 1 == len(args[1])


def test_analyze_exception(mocks):
    mocks['mock_file_service'].save_csv.side_effect = Exception('fail')

    analyze()

    mocks['mock_logger'].error.assert_called()
