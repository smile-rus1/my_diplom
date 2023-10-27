import uuid

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from search_site import models

from job_search_help_site import settings


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
    user.is_active = False
    user.save()

    if type_user == "applicant":
        _register_applicant(user)

    if type_user == "company":
        _register_company(user)

    confirm_link = create_confirm_link(request, user, type_user)
    message = (f"Ссылка на потверждение:\n%s" % confirm_link)

    # почему-то не отправляется сообщение, потом решить проблему эту! (email в ЧС отправили:( )
    send_mail(
        subject="Пожалуйста потвердите свою регистрацию на сайте rabota_help",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email, ],
        fail_silently=False
    )
    messages.success(request, "Вам на email отправлено письмо!")

    return True


def create_confirm_link(request, user: models.CustomUser, role: str):
    """
    Создает ссылку для потверждения пользователя.
    """
    token = uuid.uuid4().hex
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    cache.set(redis_key, {"user_id": user.id, "role": role}, timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT)

    confirm_link = request.build_absolute_uri(
        reverse_lazy(
            "register_confirm", kwargs={"token": token}
        )
    )
    print(f"confirm_link {confirm_link}")
    return confirm_link


def is_confirmation_user(request, user_id) -> bool:
    """
    Потверждение пользоваетеля.
    """
    try:
        user = get_object_or_404(models.CustomUser, id=user_id)
        user.is_active = True
        user.save()
        login(request, user)
        return True

    except AttributeError:
        return False


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


def check_email_in_db(email: str) -> bool:
    """
    Проверка на то, что email существует в БД.
    """
    try:
        user = models.CustomUser.objects.get(email=email)
        return True

    except models.CustomUser.DoesNotExist:
        return False


def get_link_forgot_password(request, email: str):
    """
    Восстановление забытого пароля у пользователя.
    """
    if not check_email_in_db(email):
        messages.error(request, "Такого email не существует!")
        return

    token = uuid.uuid4().hex
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    cache.set(redis_key, {"email": email}, timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT)

    recovery_link = request.build_absolute_uri(
        reverse_lazy(
            "recovery_password", kwargs={"token": token}
        )
    )
    print(f"recovery_link: {recovery_link}")
    send_mail(
        subject="Пожалуйста потвердите свою регистрацию на сайте rabota_help",
        message=f"Для восстановления пароля перейдите по ссылке {recovery_link}\nЕсли же это не Вы "
                f"восстанавливаете пароль, то просто проигнорируйте.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email, ],
        fail_silently=False
    )
    messages.success(request, "Вам на email отправлено письмо!")


def change_forgot_password(request, email: str, password1: str, password2: str) -> bool:
    """
    Меняет забытый пароль пользователя.
    """
    if not _match_password(password1, password2):
        messages.error(request, "Пароли не совпадают!")
        return False

    user = models.CustomUser.objects.filter(email=email).first()
    user.set_password(password1)
    user.save()
    return True

