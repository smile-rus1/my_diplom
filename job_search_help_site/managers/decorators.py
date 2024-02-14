from functools import wraps

from django.http import HttpResponseForbidden


def staff_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Not authenticated")

        if request.user.is_superuser:
            return HttpResponseForbidden("No access")

        if not request.user.is_staff:
            return HttpResponseForbidden("Insufficient rights")

        return view_func(self, request, *args, **kwargs)

    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Not authenticated")

        if not request.user.is_superuser:
            return HttpResponseForbidden("You don't have permissions")

        return view_func(self, request, *args, **kwargs)

    return wrapper


def personal_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Not authenticated")

        if not request.user.is_staff:
            return HttpResponseForbidden("You don't have permissions")

        return view_func(self, request, *args, **kwargs)

    return wrapper
