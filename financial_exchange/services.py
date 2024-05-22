import os
import smtplib
from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.hashers import make_password, check_password
from dotenv import load_dotenv
from django.db import transaction
from .exceptions import UserNotFound, EmailAlreadyExists
from .models import User, Transaction, Account

load_dotenv()


class UserService:
    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise UserNotFound(f"User with ID {user_id} not found.")

    @staticmethod
    def create_user(data):
        if User.objects.filter(email=data.get('email')).exists():
            raise EmailAlreadyExists(f"Email {data.get('email')} is already in use.")
        new_user = User(
            email=data.get('email'),
            password=make_password(data.get('password')),
            is_admin=data.get('is_admin' == 'Yes', False)
        )
        new_user.save()
        return new_user

    @staticmethod
    def update_user(user_id, update_data):
        user = UserService.get_user(user_id)
        if User.objects.filter(email=update_data.get('email')).exclude(pk=user_id).exists():
            raise EmailAlreadyExists(f"Email {update_data.get('email')} is already in use.")

        user.email = update_data.get('email', user.email)
        user.password = make_password(update_data.get('password', user.password))
        user.is_admin = update_data.get('is_admin', user.is_admin) == 'true'
        user.save()
        return user

    @staticmethod
    def delete_user(user_id):
        user = UserService.get_user(user_id)
        user.delete()


class AuthService:
    @staticmethod
    def register(email, password):
        if User.objects.filter(email=email).exists():
            raise EmailAlreadyExists(f"Email {email} is already in use.")
        new_user = User(email=email, password=make_password(password))
        new_user.save()
        return new_user

    @staticmethod
    def login(email, password):
        user = User.objects.get(email=email)
        if user and check_password(password, user.password):
            return user
        return None


class AccountService:
    @staticmethod
    def get_all_accounts():
        return Account.objects.all()

    @staticmethod
    def get_account(account_id):
        return Account.objects.get(pk=account_id)

    @staticmethod
    def create_account(user_id, name, balance):
        account = Account(user_id=user_id, name=name, balance=balance)
        account.save()
        return account

    @staticmethod
    def update_account(account_id, user_id, balance):
        account = Account.objects.get(pk=account_id)
        account.user = User.objects.get(pk=user_id)
        account.balance = balance
        account.save()
        return account

    @staticmethod
    def delete_account(account_id):
        account = Account.objects.get(pk=account_id)
        account.delete()

    @staticmethod
    def get_accounts_by_user(user_id):
        return Account.objects.filter(user_id=user_id)


class TransactionService:
    @staticmethod
    def get_all_transactions():
        return Transaction.objects.all()

    @staticmethod
    def get_transactions_by_account(account_id):
        return Transaction.objects.filter(account_from_id=account_id)

    @staticmethod
    def get_transaction(transaction_id):
        return Transaction.objects.get(pk=transaction_id)

    @staticmethod
    def create_transaction(from_account_id, to_account_id, amount):
        try:
            with transaction.atomic():
                from_account = Account.objects.select_for_update().get(id=from_account_id)
                to_account = Account.objects.select_for_update().get(id=to_account_id)
                amount = Decimal(amount)

                if from_account.balance < amount:
                    return False, "Insufficient funds"

                from_account.balance -= amount
                to_account.balance += amount

                from_account.save()
                to_account.save()

                Transaction.objects.create(
                    account_from=from_account,
                    account_to=to_account,
                    amount=amount
                )

                return True, "Transfer successful"
        except Account.DoesNotExist:
            return False, "Account not found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def update_transaction(transaction_id, account_from_id, account_to_id, amount):
        transaction = Transaction.objects.get(pk=transaction_id)
        transaction.account_from = Account.objects.get(pk=account_from_id)
        transaction.account_to = Account.objects.get(pk=account_to_id)
        transaction.amount = amount
        transaction.save()
        return transaction

    @staticmethod
    def delete_transaction(transaction_id):
        transaction = Transaction.objects.get(pk=transaction_id)
        transaction.delete()


class MailService:
    @staticmethod
    def send_email(recipient_email):
        # Create the message
        message = MIMEMultipart()
        message['From'] = f"{os.getenv('APP_NAME')} <{os.getenv('MAIL_USERNAME')}>"
        message['To'] = recipient_email
        message['Subject'] = 'Підтвердження створення акаунту'

        body = f"Привіт, ваш акаунт було успішно створено!"
        message.attach(MIMEText(body, 'html'))

        # Connect to the SMTP server and send the email
        try:
            with smtplib.SMTP(os.getenv('MAIL_SERVER'), int(os.getenv('MAIL_PORT'))) as server:
                server.starttls()
                server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
                server.send_message(message)
                print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")
