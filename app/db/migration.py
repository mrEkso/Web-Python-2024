import sqlite3

from app.db.database import db


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

    # Migrate Users
    users_collection = db['users']
    for user in users_data:
        users_collection.insert_one({
            "_id": user[0],
            "username": user[1],
            "hashed_password": user[2],
            "is_admin": user[3]
        })

    # Migrate Accounts
    accounts_collection = db['accounts']
    for account in accounts_data:
        accounts_collection.insert_one({
            "_id": account[0],
            "user_id": account[1],
            "balance": account[2]
        })

    # Migrate Transactions
    transactions_collection = db['transactions']
    for transaction in transactions_data:
        transactions_collection.insert_one({
            "_id": transaction[0],
            "account_id": transaction[1],
            "amount": transaction[2]
        })

    # Close sessions and connections to clean up
    sqlite_cursor.close()
    sqlite_connection.close()
