from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def user_restricted_access(view_func):
    def _wrapped_view(request, *args, **kwargs):
        username = kwargs.get('username')
        if request.user.is_authenticated:
            if request.user.username == username:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")
        else:
            return HttpResponseForbidden("Пожалуйста, войдите в систему.")
    return _wrapped_view