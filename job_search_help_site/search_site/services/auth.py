from django.contrib import messages
from django.contrib.auth import login, authenticate

from search_site.models import CustomUser


def register_applicant(request, email: str, password1: str, password2: str):
    if not _match_password(password1, password2):
        return messages.error(request, 'Пароли не совпадают')

    if not _is_valid_password(password1):
        return messages.error(request, "Пароль должен состоять из 8 символов и в нем должны быть буквы!")

    user, created = CustomUser.objects.get_or_create(email=email)

    if not created:
        return messages.error(request, "Такой email уже зарегистрирован!")

    user.set_password(password1)
    user.save()

    login_user(request, {"email": email, "password": password1})
    return True


def login_user(request, user: dict):
    user = authenticate(request, email=user["email"], password=user["password"])
    if user is not None:
        login(request, user)
    else:
        return False

    return True


def _match_password(password1: str, password2: str):
    if password1 != password2:
        return False
    return True


def _is_valid_password(password1: str):
    if len(password1) < 8:
        return False

    if not any(char.isdigit() for char in password1):
        return False

    return True
