from typing import Any

from job_search_help_site.celery import app

from . import messages


@app.task
def send_message_from_help_page(data_message: dict[str, Any]):
    """
    Создает таску на сообщение из страницы help.
    """
    messages.send_message_from_help_page_to_email(data_message)


@app.task
def send_link_confirmation_on_register(data_user: dict[str, Any]) -> None:
    """
    Создает таску на регистрацию и отправку ссыли.
    """
    messages.send_message_from_registration_page(data_user)


@app.task
def send_link_from_forgot_password_page(mail_data: dict[str, str]) -> None:
    messages.send_message_with_link_from_forgot_password_page(mail_data)
