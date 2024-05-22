from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    # User URLs
    path('users/', views.list_users, name='list_users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/update/<int:user_id>/', views.user_update, name='user_update'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),

    # Authentication URLs
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Account URLs
    path('accounts/', views.list_accounts, name='list_accounts'),
    path('accounts/my/', views.my_accounts, name='my_accounts'),
    path('accounts/<int:account_id>/', views.account_detail, name='account_detail'),
    path('accounts/admin/<int:account_id>/', views.account_detail_admin, name='account_detail_admin'),
    path('accounts/create/', views.account_create, name='account_create'),
    path('accounts/update/<int:account_id>/', views.account_update, name='account_update'),
    path('accounts/delete/<int:account_id>/', views.account_delete, name='account_delete'),

    # Transaction URLs
    path('transactions/', views.list_transactions, name='list_transactions'),
    path('transactions/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/update/<int:transaction_id>/', views.transaction_update, name='transaction_update'),
    path('transactions/delete/<int:transaction_id>/', views.transaction_delete, name='transaction_delete'),
]
