from typing import Any

from django.core.mail import send_mail

from job_search_help_site import settings


def send_message_from_registration_page(data_user: dict[str, Any]):
    """
    Присылает сообщение на почту с регистрационной формы.
    """
    send_mail(
        subject="Пожалуйста потвердите свою регистрацию на сайте rabota_help",
        message=data_user.get("message"),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[data_user.get("email"), ],
        fail_silently=False
    )


def send_message_with_link_from_forgot_password_page(mail_data: dict[str, str]):
    """
    Присылоает сообщение на почту с ссылкой на восстановление пароля.
    """
    send_mail(
        subject="Восстановление пароля",
        message=f"Для восстановления пароля перейдите по ссылке {mail_data.get('recovery_link')}"
                f"\nЕсли же это не Вы "
                f"восстанавливаете пароль, то просто проигнорируйте.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[mail_data.get('email'), ],
        fail_silently=False
    )
