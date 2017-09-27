from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mendelmd.settings')

app = Celery('mendelmd')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.config_from_object({
#     'BROKER_URL': 'django://',
#     'CELERY_RESULT_BACKEND': 'db+sqlite:///mendelmd.sqlite3',
#     'CELERYD_POOL_RESTARTS': True,  # Required for /worker/pool/restart API
# })
# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))