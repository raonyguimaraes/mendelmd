import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mendelmd.settings')

from django.conf import settings  # noqa

app = Celery('mendelmd')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    result_backend='djcelery.backends.cache:CacheBackend',
    task_always_eager=False,
    task_ignore_result=False,
    broker_url='amqp://guest:guest@queues:5672//'
)
app.conf.timezone = 'UTC'

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
