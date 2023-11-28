from typing import Any

from job_search_help_site.celery import app

from .messages import send_help_message


@app.task
def send_message_from_help_page(data_message: dict[str, Any]):
    send_help_message.send_message_from_help_page_to_email(data_message)
