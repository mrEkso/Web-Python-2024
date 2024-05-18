from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('/', views.list_users, name='list_users'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('create/', views.user_create, name='user_create'),
    path('update/<int:user_id>/', views.user_update, name='user_update'),
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
]
