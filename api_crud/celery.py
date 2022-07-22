from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_crud.settings')

app = Celery('api_crud')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()
app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')
