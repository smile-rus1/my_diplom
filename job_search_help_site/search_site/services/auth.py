from django.contrib import messages
from django.contrib.auth import login, authenticate

from search_site import models


def register_user(request, email: str, password1: str, password2: str, type_user: str) -> bool:
    """
    Регистрирует пользователя по emaul, password1, password2.
    """
    if not _match_password(password1, password2):
        return messages.error(request, 'Пароли не совпадают')

    if not _is_valid_password(password1):
        return messages.error(request, "Пароль должен состоять из 8 символов и в нем должны быть буквы!")

    user, created = models.CustomUser.objects.get_or_create(email=email)

    if not created:
        return messages.error(request, "Такой email уже зарегистрирован!")

    user.set_password(password1)
    user.save()

    if type_user == "applicant":
        _register_applicant(user)

    if type_user == "company":
        _register_company(user)

    login_user(request, {"email": email, "password": password1})
    return True


def login_user(request, user: dict) -> bool:
    """
    Авторизирует пользователя по email и password.
    """
    user = authenticate(request, email=user["email"], password=user["password"])
    if user is not None:
        login(request, user)
    else:
        return False

    return True


def check_user_role(request):
    """
    Проверяет роль пользователя.
    """
    if request.user.is_authenticated:
        user = request.user

        if hasattr(user, 'applicant'):
            return "applicant"

        elif hasattr(user, 'company'):
            return "company"
    return


def _register_applicant(user: models.CustomUser) -> None:
    """
    Регистрация роли applicant по user.
    """
    applicant, created = models.Applicant.objects.get_or_create(user=user)


def _register_company(user: models.CustomUser) -> None:
    """
    Регистрация роли applicant по company.
    """
    company, created = models.Company.objects.get_or_create(user=user)


def _match_password(password1: str, password2: str) -> bool:
    """
    Проверка паролей на совпадение.
    """
    if password1 != password2:
        return False
    return True


def _is_valid_password(password1: str) -> bool:
    """
    Проверка пароля на валидацию.
    """
    if len(password1) < 8:
        return False

    if not any(char.isdigit() for char in password1):
        return False

    return True
