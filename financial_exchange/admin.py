from django.contrib import admin
from .models import User, Account, Transaction


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_admin']
    search_fields = ['email']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
    search_fields = ['user__email']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account_from', 'account_to', 'amount', 'date']
    search_fields = ['account__user__email']
