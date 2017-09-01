# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import Celery
app = Celery('mendelmd')

from tasks.models import Task
from workers.models import Worker

from django.db.models import Q

@app.task
def check_queue():
    #check tasks and launch workers if necessary
    print('check queue')
    tasks = Task.objects.filter(status='new')
    workers = Worker.objects.filter(Q(status='new') | Q(status='running'))
    n_tasks = len(tasks)
    n_workers = len(workers)
    # print(tasks, len(tasks))
    # print(workers, len(workers))
    #if there are things in the queue launch worker
    if n_tasks > 0 and n_workers < n_tasks:
        # launch more workers
        workers_launch = n_tasks-n_workers
        print('workers_launch', workers_launch)
        for i in range(0, workers_launch):
            print('Launch ', i)
    #install and launch workers
    #if there are not more items to be processed in the queue
    #turn off workers
