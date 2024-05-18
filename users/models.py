class User:
    def __init__(self, email, password, is_admin=False, id=None):
        self.id = id
        self.email = email
        self.password = password
        self.is_admin = is_admin


class Account:
    def __init__(self, user_id, balance=0.0, id=None):
        self.id = id
        self.user_id = user_id
        self.balance = balance


class Transaction:
    def __init__(self, account_id, amount, id=None):
        self.id = id
        self.account_id = account_id
        self.amount = amount
