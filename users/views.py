from threading import Thread

from django.shortcuts import render, redirect

from .exceptions import EmailAlreadyExists, UserNotFound
from .services import UserService, MailService


def list_users(request):
    users = UserService.get_all_users()
    return render(request, 'users/list.html', {'users': users})


def user_detail(request, user_id):
    try:
        user = UserService.get_user(user_id)
        return render(request, 'users/detail.html', {'user': user})
    except UserNotFound:
        return render(request, '404.html', status=404)


def user_create(request):
    if request.method == 'POST':
        try:
            new_user = UserService.create_user(request.POST)
            # Send email in a separate thread
            Thread(target=MailService.send_email, args=new_user.email).start()
            return render(request, 'users/detail.html', {'user': new_user})
        except EmailAlreadyExists as e:
            return render(request, 'users/create.html', {'error': str(e), 'form_data': request.POST})
    return render(request, 'users/create.html')


def user_update(request, user_id):
    user = UserService.get_user(user_id)
    if request.method == 'POST':
        try:
            updated_user = UserService.update_user(user_id, request.POST)
            return render(request, 'users/detail.html', {'user': updated_user})
        except EmailAlreadyExists as e:
            return render(request, 'users/update.html', {'error': str(e), 'user': user, 'form_data': request.POST})
    return render(request, 'users/update.html', {'user': user})


def user_delete(request, user_id):
    UserService.delete_user(user_id)
    return redirect('users:list_users')
