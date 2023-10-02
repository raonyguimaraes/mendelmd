from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rockbio.settings')

from django.conf import settings  # noqa

app = Celery('rockbio',broker_connection_retry_on_startup=True)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.broker_transport_options = {'visibility_timeout': 43200}

# app.conf.update(
#     CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
# )

app.conf.update(
    CELERY_RESULT_BACKEND='django-db',
)
app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

