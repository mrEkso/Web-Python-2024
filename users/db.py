from users.models import User, Account, Transaction

users = [
    User(id=1, email='alice@example.com', password='password123', is_admin=True),
    User(id=2, email='bob@example.com', password='password456', is_admin=False)
]
accounts = [
    Account(id=1, user_id=1, balance=1000.0),
    Account(id=2, user_id=2, balance=1500.0)
],
transactions = [
    Transaction(id=1, account_id=1, amount=100.0),
    Transaction(id=2, account_id=1, amount=-50.0),
    Transaction(id=3, account_id=2, amount=200.0),
    Transaction(id=4, account_id=2, amount=-100.0)
]
