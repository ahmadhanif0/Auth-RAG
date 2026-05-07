import os
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


async def send_email(to_email: str, subject: str, body: str):

    message = EmailMessage()
    message["From"] = os.getenv("FROM_EMAIL")
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")

    await aiosmtplib.send(
        message,
        hostname=smtp_server,
        port=smtp_port,
        start_tls=True,
        username=smtp_user,
        password=smtp_pass,
    )