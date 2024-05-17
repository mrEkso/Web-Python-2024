import sqlite3

from passlib.context import CryptContext

from app.db.database import db

# CryptContext instance for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def migrate_db():
    # Connect to SQLite
    sqlite_connection = sqlite3.connect('./financial_exchange.db')
    sqlite_cursor = sqlite_connection.cursor()

    # Fetch data
    sqlite_cursor.execute("SELECT * FROM users")
    users_data = sqlite_cursor.fetchall()

    sqlite_cursor.execute("SELECT * FROM accounts")
    accounts_data = sqlite_cursor.fetchall()

    sqlite_cursor.execute("SELECT * FROM transactions")
    transactions_data = sqlite_cursor.fetchall()

    user_ids_map = {}
    account_ids_map = {}

    # Migrate Users
    users_collection = db['users']
    for user in users_data:
        new_user = {
            "username": user[1],
            "hashed_password": pwd_context.hash(user[2]),  # hash the password
            "is_admin": user[3]
        }
        result = users_collection.insert_one(new_user)
        user_ids_map[user[0]] = result.inserted_id

    # Migrate Accounts
    accounts_collection = db['accounts']
    for account in accounts_data:
        new_account = {
            "user_id": user_ids_map[account[1]],
            "balance": account[2]
        }
        result = accounts_collection.insert_one(new_account)
        account_ids_map[account[0]] = result.inserted_id

    # Migrate Transactions
    transactions_collection = db['transactions']
    for transaction in transactions_data:
        new_transaction = {
            "account_id": account_ids_map[transaction[1]],
            "amount": transaction[2]
        }
        transactions_collection.insert_one(new_transaction)

    # Close sessions and connections to clean up
    sqlite_cursor.close()
    sqlite_connection.close()
