import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()


def send_email(subject,body,to_email):
    SMTP_SERVER = os.getenv('EMAIL_HOST')
    SMTP_PORT = os.getenv('EMAIL_PORT')

    sender_email = os.getenv('EMAIL_HOST_USER')
    password = os.getenv('EMAIL_HOST_PASSWORD')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    # message.attach(MIMEText(body, 'plain'))
    message.attach(MIMEText(body, 'html'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    return True
