from job_search_help_site.celery import app
from managers.services.send_notifications import SendEmailNotifications


@app.task
def send_notifications_email(data_message: dict):
    """
    Sends notifications on email.
    """
    SendEmailNotifications().send_notification(data_message)
