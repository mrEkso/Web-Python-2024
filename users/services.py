import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from passlib.context import CryptContext

from .db import users
from .exceptions import UserNotFound, EmailAlreadyExists
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    def get_all_users():
        return users

    @staticmethod
    def get_user(user_id):
        user = next((user for user in users if user.id == user_id), None)
        print(user.password)
        if not user:
            raise UserNotFound(f"User with ID {user_id} not found.")
        return user

    @staticmethod
    def create_user(data):
        if any(u.email == data.get('email') for u in users):
            raise EmailAlreadyExists(f"Email {data.get('email')} is already in use.")

        new_user = User(
            id=max((user.id for user in users), default=0) + 1,
            email=data.get('email'),
            password=pwd_context.hash(data.get('password')),
            is_admin=data.get('is_admin') == 'true'
        )
        users.append(new_user)
        return new_user

    @staticmethod
    def update_user(user_id, update_data):
        user = UserService.get_user(user_id)
        if any(u.email == update_data.get('email') and u.id != user_id for u in users):
            raise EmailAlreadyExists(f"Email {update_data.get('email')} is already in use.")
        if user:
            user.email = update_data.get('email', user.email)
            user.password = pwd_context.hash(update_data.get('password', user.password))
            user.is_admin = update_data.get('is_admin', user.is_admin) == 'true'
        return user

    @staticmethod
    def delete_user(user_id):
        global users
        users = [user for user in users if user.id != user_id]


class MailService:
    @staticmethod
    def send_email(recipient_email):
        # Create the message
        message = MIMEMultipart()
        message['From'] = os.getenv('MAIL_FROM_NAME') + " <" + os.getenv('MAIL_FROM') + ">"
        message['To'] = recipient_email
        message['Subject'] = 'Підтвердження створення акаунту'

        body = f"Привіт, ваш акаунт було успішно створено!"
        message.attach(MIMEText(body, 'html'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(os.getenv('MAIL_SERVER'), int(os.getenv('MAIL_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
            server.send_message(message)
