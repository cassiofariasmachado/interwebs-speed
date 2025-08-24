import pytest
from typer.testing import CliRunner
from interwebs_speed.cli import app
from unittest.mock import patch, MagicMock

runner = CliRunner()

def test_version_command():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "interwebs-speed v0.1.0" in result.stdout

@patch('interwebs_speed.cli.analisys_service')
def test_analyze_command(mock_analisys_service):
    result = runner.invoke(app, ["analyze"])
    assert result.exit_code == 0
    mock_analisys_service.analyze.assert_called_once()

@patch('interwebs_speed.cli.summary_service')
def test_summary_command_current_month(mock_summary_service):
    result = runner.invoke(app, ["summary"])
    assert result.exit_code == 0
    mock_summary_service.send_monthly_summary.assert_called_once_with(False)

@patch('interwebs_speed.cli.summary_service')
def test_summary_command_previous_month(mock_summary_service):
    result = runner.invoke(app, ["summary", "--previous-month"])
    assert result.exit_code == 0
    mock_summary_service.send_monthly_summary.assert_called_once_with(True)

@patch('interwebs_speed.cli.summary_service')
def test_summary_command_previous_month_short_flag(mock_summary_service):
    result = runner.invoke(app, ["summary", "-p"])
    assert result.exit_code == 0
    mock_summary_service.send_monthly_summary.assert_called_once_with(True)
