from django.shortcuts import render, redirect

from .services import UserService


def list_users(request):
    users = UserService.get_all_users()
    return render(request, 'users/list.html', {'users': users})


def user_detail(request, user_id):
    try:
        user = UserService.get_user(user_id)
        return render(request, 'users/detail.html', {'user': user})
    except UserService.UserNotFound:
        return render(request, '404.html', status=404)


def user_create(request):
    if request.method == 'POST':
        new_user = UserService.create_user(request.POST)
        return render(request, 'users/detail.html', {'user': new_user})
    return render(request, 'users/create.html')


def user_update(request, user_id):
    if request.method == 'POST':
        updated_user = UserService.update_user(user_id, request.POST)
        return render(request, 'users/detail.html', {'user': updated_user})
    return render(request, 'users/update.html', {'user': UserService.get_user(user_id)})


def user_delete(request, user_id):
    UserService.delete_user(user_id)
    return redirect('users:list_users')
