import pytest
from unittest.mock import patch, MagicMock
from interwebs_speed.services.internet_speed_service import get_internet_speed
from interwebs_speed.core.analisys import Analysis

@patch('interwebs_speed.services.internet_speed_service.speedtest.Speedtest')
def test_get_internet_speed(mock_speedtest):
    mock_instance = MagicMock()
    mock_instance.results.dict.return_value = {
        'download': 100000000,
        'upload': 50000000,
        'ping': 10.0
    }
    mock_speedtest.return_value = mock_instance

    analysis = get_internet_speed()

    mock_speedtest.assert_called_once_with(secure=True)
    mock_instance.get_servers.assert_called_once()
    mock_instance.get_best_server.assert_called_once()
    mock_instance.download.assert_called_once()
    mock_instance.upload.assert_called_once()
    mock_instance.results.dict.assert_called_once()

    assert isinstance(analysis, Analysis)
    assert analysis.download == 100000000
    assert analysis.upload == 50000000
    assert analysis.ping == pytest.approx(10.0)
