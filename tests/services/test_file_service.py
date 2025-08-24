import pytest
from unittest.mock import mock_open, patch
from interwebs_speed.services.file_service import save_csv, exists

@patch('builtins.open', new_callable=mock_open)
def test_save_csv_write_mode(mock_file):
    file_path = "test.csv"
    lines = ["header", "data1", "data2"]
    save_csv(file_path, lines, mode='w')
    mock_file.assert_called_once_with(file_path, 'w', encoding='utf-8')
    mock_file().write.assert_called_once_with("header\ndata1\ndata2\n")

@patch('builtins.open', new_callable=mock_open)
def test_save_csv_append_mode(mock_file):
    file_path = "test.csv"
    lines = ["data3"]
    save_csv(file_path, lines, mode='a')
    mock_file.assert_called_once_with(file_path, 'a', encoding='utf-8')
    mock_file().write.assert_called_once_with("data3\n")

@patch('os.path.isfile')
def test_exists_true(mock_isfile):
    mock_isfile.return_value = True
    file_path = "existing_file.csv"
    assert exists(file_path) is True
    mock_isfile.assert_called_once_with(file_path)

@patch('os.path.isfile')
def test_exists_false(mock_isfile):
    mock_isfile.return_value = False
    file_path = "non_existing_file.csv"
    assert exists(file_path) is False
    mock_isfile.assert_called_once_with(file_path)
