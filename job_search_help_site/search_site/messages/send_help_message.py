from django.core.mail import send_mail

from job_search_help_site import settings


def send_message_from_help_page_to_email(topic: str, content: str, email: str, fullname: str):
    """
    Отправляет сообщение со страницы help, на главную почту разработчика.
    """
    send_mail(
        topic,
        f"Адрес отправителя: {email}\n\nПолное имя отправителя: {fullname}\nСообщение:\n{content}",
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False
    )
    return True
