from django.db import models
from django.utils import timezone


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'accounts'


class Transaction(models.Model):
    account_from = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_from')
    account_to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_to')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'transactions'
