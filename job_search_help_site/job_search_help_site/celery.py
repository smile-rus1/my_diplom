import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_search_help_site.settings')

app = Celery("job_search_help_site")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
