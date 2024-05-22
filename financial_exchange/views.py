from threading import Thread

from django.contrib.auth import login
from django.shortcuts import render, redirect

from .decorators import admin_required, login_required
from .exceptions import EmailAlreadyExists, UserNotFound
from .forms import UserForm
from .services import UserService, MailService, TransactionService, AccountService, AuthService


@login_required
def welcome(request):
    user = UserService.get_user(request.session.get('user_id'))
    return render(request, 'welcome.html', {'is_admin': user.is_admin})


# User Views
@admin_required
def list_users(request):
    users = UserService.get_all_users()
    return render(request, 'users/list.html', {'users': users})


@admin_required
def user_detail(request, user_id):
    try:
        user = UserService.get_user(user_id)
        return render(request, 'users/detail.html', {'user': user})
    except UserNotFound:
        return render(request, '404.html', status=404)


@admin_required
def user_create(request):
    if request.method == 'POST':
        try:
            new_user = UserService.create_user(request.POST)
            # Send email in a separate thread
            Thread(target=MailService.send_email, args=(new_user.email,)).start()
            return render(request, 'users/detail.html', {'user': new_user})
        except EmailAlreadyExists as e:
            return render(request, 'users/create.html', {'error': str(e), 'form_data': request.POST})
    return render(request, 'users/create.html')


@admin_required
def user_update(request, user_id):
    user = UserService.get_user(user_id)
    if request.method == 'POST':
        try:
            updated_user = UserService.update_user(user_id, request.POST)
            return render(request, 'users/detail.html', {'user': updated_user})
        except EmailAlreadyExists as e:
            return render(request, 'users/update.html', {'error': str(e), 'user': user, 'form_data': request.POST})
    return render(request, 'users/update.html', {'user': user})


@admin_required
def user_delete(request, user_id):
    UserService.delete_user(user_id)
    return redirect('users:list_users')


# Authentication Views
def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = AuthService.register(form.cleaned_data['email'], form.cleaned_data['password'])
            Thread(target=MailService.send_email, args=(new_user.email,)).start()
            request.session['user_id'] = new_user.id
            return redirect('welcome')
        else:
            return render(request, 'auth/register.html', {'error': EmailAlreadyExists, 'form_data': request.POST})
    return render(request, 'auth/register.html')


def user_login(request):
    if request.method == 'POST':
        user = AuthService.login(request.POST['email'], request.POST['password'])
        if user:
            request.session['user_id'] = user.id
            return redirect('welcome')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid email or password'})
    return render(request, 'auth/login.html')


@login_required
def user_logout(request):
    request.session.flush()
    return redirect('login')


# Account Views
@admin_required
def list_accounts(request):
    accounts = AccountService.get_all_accounts()
    return render(request, 'accounts/list.html', {'accounts': accounts})


@login_required
def my_accounts(request):
    user_id = request.session.get('user_id')
    accounts = AccountService.get_accounts_by_user(user_id)
    return render(request, 'accounts/my_accounts.html', {'accounts': accounts})


@login_required
def account_detail(request, account_id):
    account = AccountService.get_account(account_id)
    transactions = TransactionService.get_transactions_by_account(account_id)
    return render(request, 'accounts/detail.html', {'account': account, 'transactions': transactions})


@admin_required
def account_detail_admin(request, account_id):
    account = AccountService.get_account(account_id)
    transactions = TransactionService.get_transactions_by_account(account_id)
    return render(request, 'accounts/detail_admin.html', {'account': account, 'transactions': transactions})


@login_required
def account_create(request):
    if request.method == 'POST':
        new_account = AccountService.create_account(
            user_id=request.session['user_id'],
            name=request.POST['name'],
            balance=request.POST['balance']
        )
        return redirect('account_detail', account_id=new_account.id)
    return render(request, 'accounts/create.html')


@admin_required
def account_update(request, account_id):
    users = UserService.get_all_users()
    account = AccountService.get_account(account_id)
    if request.method == 'POST':
        updated_account = AccountService.update_account(
            account_id=account_id,
            user_id=request.POST['user'],
            balance=request.POST['balance']
        )
        return redirect('account_detail_admin', account_id=updated_account.id)
    return render(request, 'accounts/update.html', {'account': account, 'users': users})


@admin_required
def account_delete(request, account_id):
    AccountService.delete_account(account_id)
    return redirect('list_accounts')


# Transaction Views
@admin_required
def list_transactions(request):
    transactions = TransactionService.get_all_transactions()
    return render(request, 'transactions/list.html', {'transactions': transactions})


@login_required
def transaction_detail(request, transaction_id):
    transaction = TransactionService.get_transaction(transaction_id)
    return render(request, 'transactions/detail.html', {'transaction': transaction})


@login_required
def transaction_create(request):
    user_id = request.session['user_id']
    accounts = AccountService.get_accounts_by_user(user_id)
    if request.method == 'POST':
        success, message = TransactionService.create_transaction(request.POST.get('from_account'),
                                                                 request.POST.get('to_account'),
                                                                 request.POST.get('amount'))
        if success:
            return render(request, 'accounts/my_accounts.html', {'success': message, 'accounts': accounts})
        else:
            return render(request, 'accounts/my_accounts.html', {'error': message, 'accounts': accounts})
    return render(request, 'accounts/my_accounts.html', {'accounts': accounts})


@login_required
def transaction_update(request, transaction_id):
    accounts = AccountService.get_all_accounts()
    transaction = TransactionService.get_transaction(transaction_id)
    if request.method == 'POST':
        updated_transaction = TransactionService.update_transaction(
            transaction_id=transaction_id,
            account_from_id=request.POST['account_from'],
            account_to_id=request.POST['account_to'],
            amount=request.POST['amount']
        )
        return redirect('transaction_detail', transaction_id=updated_transaction.id)
    return render(request, 'transactions/update.html', {'transaction': transaction, 'accounts': accounts})


@admin_required
def transaction_delete(request, transaction_id):
    TransactionService.delete_transaction(transaction_id)
    return redirect('list_transactions')
