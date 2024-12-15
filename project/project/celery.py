import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = False


app.conf.beat_schedule = {
    'send_new_posts_every_week': {
        'task': 'news_portal.tasks.task_every_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday')
    },
}