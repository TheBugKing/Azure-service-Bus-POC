import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from setting import SMTP_PASSWORD, SENDER_EMAIL, SMTP_SERVER
from log import logger


def send_mail(receiver_email=None, subject=None, message=None):
    """
    Send an email using SMTP.

    Args:
        receiver_email (str): Email address of the recipient.
        subject (str): Subject of the email.
        message (str): Body content of the email.

    Returns:
        str: Success message or error message.
    """
    if not receiver_email or not subject or not message:
        raise ValueError("receiver_email, subject, and message cannot be empty")

    # Email configuration
    sender_email = SENDER_EMAIL
    receiver_email = receiver_email

    # Set up the MIME object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to SMTP server
    smtp_server = SMTP_SERVER
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = SMTP_PASSWORD

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        logger.info("Email sent successfully!")
        return "Email sent successfully!"
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        logger.error(error_msg)
        return error_msg
