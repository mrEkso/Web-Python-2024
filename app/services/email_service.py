from fastapi_mail import FastMail, MessageSchema
from app.config.mail_config import mail_config


async def send_email(email_to: str, email: str):
    message = MessageSchema(
        subject='Підтвердження створення акаунту',
        recipients=[email_to],
        body=f"Привіт {email}, ваш акаунт було успішно створено!",
        subtype="html"
    )

    fm = FastMail(mail_config)
    await fm.send_message(message)
