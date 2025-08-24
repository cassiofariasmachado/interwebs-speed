import pytest
from unittest.mock import patch, MagicMock
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from interwebs_speed.services.mail_service import send_email, create_email

@pytest.fixture
def mock_config():
    return {
        'smtp_host': 'smtp.example.com',
        'smtp_port': 465,
        'smtp_username': 'user@example.com',
        'smtp_password': 'password',
        'alert_sender_mail': 'sender@example.com',
        'alert_receiver_mail': 'receiver@example.com'
    }

@patch('interwebs_speed.services.mail_service.smtplib.SMTP_SSL')
def test_send_email(mock_smtp_ssl, mock_config):
    mock_server = MagicMock()
    mock_smtp_ssl.return_value.__enter__.return_value = mock_server

    subject = "Test Subject"
    message = "Test Message"
    subtype = "plain"

    send_email(mock_config, subject, message, subtype)

    mock_smtp_ssl.assert_called_once_with(mock_config['smtp_host'], mock_config['smtp_port'])
    mock_server.login.assert_called_once_with(mock_config['smtp_username'], mock_config['smtp_password'])
    mock_server.sendmail.assert_called_once()

    # Check the arguments passed to sendmail
    call_args, _ = mock_server.sendmail.call_args
    assert call_args[0] == mock_config['alert_sender_mail']
    assert call_args[1] == mock_config['alert_receiver_mail']
    assert isinstance(call_args[2], str) # The email content is a string

    # Verify that create_email was called correctly
    mock_create_email_patch = patch('interwebs_speed.services.mail_service.create_email')
    mock_create_email = mock_create_email_patch.start()
    mock_create_email.return_value = MIMEMultipart() # Mock the return value of create_email
    send_email(mock_config, subject, message, subtype)
    mock_create_email.assert_called_once_with(subject, message, mock_config['alert_sender_mail'], mock_config['alert_receiver_mail'], subtype)
    mock_create_email_patch.stop()


def test_create_email(mock_config):
    subject = "Test Subject"
    message = "Test Message"
    subtype = "plain"

    mail = create_email(subject, message, mock_config['alert_sender_mail'], mock_config['alert_receiver_mail'], subtype)

    assert isinstance(mail, MIMEMultipart)
    assert mail["From"] == mock_config['alert_sender_mail']
    assert mail["To"] == mock_config['alert_receiver_mail']
    assert mail["Subject"] == subject
    assert mail.get_payload()[0].get_payload() == message
    assert mail.get_payload()[0].get_content_subtype() == subtype
