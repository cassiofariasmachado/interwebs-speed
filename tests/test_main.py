import pytest
from unittest.mock import patch, MagicMock
from interwebs_speed.__main__ import main
from interwebs_speed import __app_name__

@patch('interwebs_speed.__main__.cli')
def test_main_function(mock_cli):
    main()
    mock_cli.app.assert_called_once_with(prog_name=__app_name__)
