from django.http import HttpResponse
from functools import wraps

from django.shortcuts import redirect

from financial_exchange.services import UserService


def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect(f'/login/?next={request.path}')
        if not getattr(UserService.get_user(request.session.get('user_id')), 'is_admin', False):
            return HttpResponse("Forbidden", status=403)
        return function(request, *args, **kwargs)

    return wrap


def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect(f'/login/?next={request.path}')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
