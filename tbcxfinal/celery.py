import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tbcxfinal.settings')

app = Celery('tbcxfinal')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'check-every-2-minutes': {
        'task': 'votes.tasks.check_voting',
        'schedule': 60.0,  # crontab(hour=0, minute=0)
    },
    'get-popular-products': {
        'task': 'main.tasks.popular_locations',
        'schedule': 60.0,
        'args': ('popular_locations',)  # Cache key
    },
}
