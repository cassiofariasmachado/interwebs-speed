from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email(config: dict, subject: str, message: str):
    host = config.get('smtp_host')
    port = config.get('smtp_port')

    username = config.get('smtp_username')
    password = config.get('smtp_password')

    sender = config.get('alert_sender_mail')
    receiver = config.get('alert_receiver_mail')

    email = create_email(subject, message, sender, receiver)

    with smtplib.SMTP_SSL(host, port) as server:
        server.login(username, password)
        server.sendmail(sender, receiver, email.as_string())


def create_email(subject: str, message: str, sender: str, receiver: str) -> MIMEMultipart:
    mail = MIMEMultipart()

    mail["From"] = sender
    mail["To"] = receiver
    mail["Subject"] = subject

    mail.attach(MIMEText(message, "plain"))

    return mail
