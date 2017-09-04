# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import Celery
app = Celery('mendelmd')

from tasks.models import Task
from workers.models import Worker
from django.db.models import Q
from scripts.worker import IWorker

from subprocess import run

@app.task
def launch_workers(n_workers):
    for i in range(0, n_workers):
        print('Launch ', i)
        # launch new worker
        worker = Worker()
        worker.name = 'New Worker'
        worker_result = IWorker().launch()
        worker.ip = worker_result['ip']
        worker.worker_id = worker_result['id']
        worker.status = 'new'
        worker.save()

@app.task
def terminate_workers():
    idle_workers = Worker.objects.filter(status='idle')
    for worker in idle_workers:
        print('Terminate Worker')
        # Terminate_Worker()

@app.task
def terminate_worker(worker_id):
    worker = Worker.objects.get(id=worker_id)
    print('Terminate Worker', worker.id)

@app.task
def install_worker(worker_id):
    worker = Worker.objects.get(id=worker_id)
    print('Install Worker', worker.id)
    #copy install script to worker

    params = "-o 'StrictHostKeyChecking=no' -o 'UserKnownHostsFile=/dev/null'"

    command = "scp %s scripts/install_worker_ubuntu.sh ubuntu@%s:~/" % (params, worker.ip)
    run(command, shell=True)

    command = """nohup bash install_worker_ubuntu.sh 2>&1 & sleep 1"""
    command = """ssh %s -t ubuntu@%s '%s'""" % (
        params, worker.ip, command)
    run(command, shell=True)