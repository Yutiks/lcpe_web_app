from celery import Celery
from celery.schedules import crontab
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lcpe.settings')
broker_url = os.environ.get('CELERY_URL')

app = Celery('lcpe', broker=broker_url)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'send-training-reminders-every-minute': {
        'task': 'training.tasks.send_training_reminders',
        'schedule': crontab(minute='*'),
    },
}

