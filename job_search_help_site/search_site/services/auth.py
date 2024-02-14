import uuid

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from search_site import models

from job_search_help_site import settings
from .. import tasks


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

    data_user = {
        "message": message,
        "email": email
    }
    tasks.send_link_confirmation_on_register.delay(data_user)
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

        if user.is_superuser:
            return "is_superuser"

        elif user.is_staff:
            return "is_staff"
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
    mail_data = {
        "recovery_link": recovery_link,
        "email": email
    }
    tasks.send_link_from_forgot_password_page.delay(mail_data)
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


def create_confirm_link_role(request) -> str:
    """
    Создает ссылку для потверждения роли пользователя и возвращает ее.
    """
    token = uuid.uuid4().hex
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    cache.set(redis_key, {
        "user_role_conf_id": request.user.id,
        "user_role_conf": check_user_role(request)
    },
              timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT
              )

    confirm_link = request.build_absolute_uri(
            reverse_lazy(
                "confirm_users_role", kwargs={"token": token}
            )
        )
    return confirm_link


def confirm_role_users(request) -> None:
    """
    Потверждение у пользователя его роли.
    """
    role = "компании" if check_user_role(request) == "company" else "кандидата"
    link_confirmed = create_confirm_link_role(request)

    data_message = {
        "subject": f"Проверка {role} на подлинность",
        "message": f"«Здравствуйте!\n"
                   f"Вы решили подтвердить свою роль на нашем сайте. "
                   f"Для дальнейшего подтверждения, перейдите по ссылке, которая будет указана ниже, "
                   f"чтобы мы могли связаться с Вами.»\n"
                   f"\nСсылка для потверждения: {link_confirmed}",
        "email_recipient": request.user.email
    }
    tasks.send_message_on_email.apply_async(args=(data_message,), countdown=15)
    print(f"LINK CONFIRM_USER: {link_confirmed}")

    messages.success(request, "Вам на email отправлено письмо с потверждением!")


def create_request_to_confirm(request, user_id: int) -> bool:
    """
    Создает запрос на потверждение пользователя для админов.
    """
    try:
        with transaction.atomic():
            user = models.CustomUser.objects.get(id=int(user_id))
            models.RequestToVerificationUser.objects.create(
                user=user,
                role=check_user_role(request)
            )
        messages.success(request, "Заявка на рассмотрение отправлена!")

    except models.CustomUser.DoesNotExist:
        messages.error(request, "Что-то пошло не так, поробуйте чуть позже!")
        return False

    except Exception as e:
        messages.error(request, "Возникла не предвиденная ошибка, попробуйте чуть позже!")
    return True
