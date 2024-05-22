from django import forms
from pydantic import ValidationError

from .models import User, Account, Transaction


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['user', 'name', 'balance']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account_from', 'account_to', 'amount']
