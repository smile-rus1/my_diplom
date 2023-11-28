from typing import Any

from django.core.mail import send_mail

from job_search_help_site import settings


def send_message_from_help_page_to_email(data_message: dict[str, Any]):
    """
    Отправляет сообщение со страницы help, на главную почту разработчика.
    """
    send_mail(
        data_message.get("topic"),
        f"Адрес отправителя: {data_message.get('email')}\n\nПолное имя отправителя: "
        f"{data_message.get('fullname')}\nСообщение:\n{data_message.get('content')}",
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False
    )
    return True
