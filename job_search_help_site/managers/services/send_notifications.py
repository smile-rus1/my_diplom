from abc import ABC, abstractmethod

from django.core.mail import send_mail

from job_search_help_site import settings
from job_search_help_site.celery import app


class SendNotifications(ABC):
    @abstractmethod
    def send_notification(self, **data):
        ...


class SendEmailNotifications(SendNotifications):
    def send_notification(self, data: dict) -> None:
        """
        Sends a confirmation email to the user.
        """
        send_mail(
            subject=data.get("subject"),
            message=data.get("message"),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data.get("email_recipient")],
            fail_silently=False
        )
