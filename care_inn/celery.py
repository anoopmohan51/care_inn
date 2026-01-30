"""
Celery configuration for care_inn project.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_inn.settings')

app = Celery('care_inn')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat schedule - runs every minute
app.conf.beat_schedule = {
    'run-workorder-escalations-every-minute': {
        'task': 'workorder_api.tasks.escalation.workorder_escalations.workorder_escalations_task',
        'schedule': crontab(minute='*'),  # Every minute
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')