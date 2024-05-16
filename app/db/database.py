import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.models import User, Account, Transaction, Base

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def init_data():
    """Populate the database with initial data."""
    session = SessionLocal()
    # Creating sample users
    user1 = User(username='john_doe', hashed_password='hashedpassword123', is_admin=False)
    user2 = User(username='admin_user', hashed_password='secureadminpass', is_admin=True)
    session.add_all([user1, user2])

    # Commit to save the new users
    session.commit()

    # Creating accounts linked to the users
    account1 = Account(user_id=user1.id, balance=1000.0)
    account2 = Account(user_id=user2.id, balance=5000.0)
    session.add_all([account1, account2])

    # Commit accounts
    session.commit()

    # Creating transactions
    transaction1 = Transaction(account_id=account1.id, amount=150.0)
    transaction2 = Transaction(account_id=account2.id, amount=-200.0)
    session.add_all([transaction1, transaction2])

    # Final commit
    session.commit()
    session.close()
