# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import Celery
app = Celery('mendelmd')

from tasks.models import Task
from workers.models import Worker
from django.db.models import Q
from workers.tasks import launch_workers, terminate_workers

@app.task
def check_queue():
    #check tasks and launch workers if necessary
    print('Check Queue')
    max_workers = 4
    tasks = Task.objects.filter(status='new')
    workers = Worker.objects.filter(Q(status='new') | Q(status='running'))
    n_tasks = len(tasks)
    n_workers = len(workers)
    #if more tasks than workers, launch workers
    if n_tasks > n_workers and n_workers < max_workers:
        n_workers_to_launch = min(n_tasks, max_workers - n_workers)
        print('Launch Workers', n_workers_to_launch)
        launch_workers(n_workers_to_launch)
    #if more workers than tasks, terminate workers
    if n_tasks < n_workers:
        print('Terminate Workers')
        terminate_workers()

@app.task
def annotate_vcf(task_id):
    task = Task.objects.get(pk=task_id)
    print('Annotate VCF', task)
