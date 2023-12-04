from typing import Any

from django.core.mail import send_mail

from job_search_help_site import settings


def send_mail_to_users(data: dict[str, Any]) -> None:
    """
    Присылает сообщение кандидату, о приглашении компании на вакансию.
    """
    send_mail(
        subject=f"{data.get('subject')}",
        message=f"{data.get('message')}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[data.get("email_recipient"), ],
        fail_silently=False
    )
