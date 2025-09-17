from pathlib import Path

from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from starlette.datastructures import URL

from src.conf.config import settings
from src.services.crypt import create_jwt_token

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
    VALIDATE_CERTS=settings.MAIL_VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(__file__).parent / "../templates",
)


async def send_email(email: EmailStr, username: str, base_url: URL):
    token = create_jwt_token(str(email))
    message = MessageSchema(
        subject="Confirm your email",
        recipients=[email],
        template_body={
            "base_url": str(base_url).rstrip("/"),
            "username": username,
            "token": token,
        },
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email_confirmation.html")


def send_email_in_background(
    email: EmailStr,
    username: str,
    base_url: URL,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(send_email, email, username, base_url)
