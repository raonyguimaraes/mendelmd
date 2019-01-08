# Create your tasks here
from __future__ import absolute_import, unicode_literals

from django.conf import settings  # noqa
from celery import Celery
app = Celery('mendelmd')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from tasks.models import Task
from workers.models import Worker
from django.db.models import Q

from subprocess import run, check_output

from helpers.scw_wrapper import SCW
from helpers.aws_wrapper import AWS

from settings.models import Provider

@app.task(queue="master")
def check_queue():
    #check tasks and launch workers if necessary
    print('Check Queue')
    max_workers = 50
    tasks = Task.objects.filter(status='scheduled')
    workers = Worker.objects.filter(~Q(status='terminated'))
    n_tasks = len(tasks)
    n_workers = len(workers)
    print(n_tasks, n_workers)
    #if more tasks than workers, launch more workers
    if n_tasks > n_workers and n_workers < max_workers:
        n_workers_to_launch = min(n_tasks, max_workers - n_workers)
        print('Launch Workers', n_workers_to_launch)
        for i in range(0,n_workers_to_launch):
            launch_worker.delay()
    #if more workers than tasks, terminate workers
    if n_tasks < n_workers:
        print('Terminate Workers')
        terminate_workers()

@app.task(queue="master")
def launch_worker():
    #create workers
    worker = Worker()
    worker.name = 'New Worker'
    worker.status = 'new'
    worker.save()

    if settings.DEFAULT_PROVIDER == 'AWS':
        provider = Provider.objects.filter(name='AWS')[0]
        print(provider, provider.config)
        worker_result = AWS().launch(provider.config)
        worker.provider = 'AWS'
        worker.type = provider.config['instance_type']
    else:
        worker_result = SCW().launch(provider.config)
        worker.provider = 'SCW'
        worker.type = ''

    worker.ip = worker_result['ip']
    worker.worker_id = worker_result['id']
    worker.save()
    install_worker.delay(worker.id)


@app.task(queue="master")
def launch_workers(n_workers, type):
    #create workers
    workers = []
    for i in range(0, int(n_workers)):
        worker = Worker()
        worker.name = 'New Worker'
        worker.type = type
        worker.status = 'new'
        worker.save()
        workers.append(worker)

    for i, worker in enumerate(workers):
        print('Launch ', i)
        # launch new worker
        worker_result = SCW().launch(type)
        worker.ip = worker_result['ip']
        worker.worker_id = worker_result['id']
        worker.save()
        install_worker.delay(worker.id)

@app.task(queue="master")
def terminate_workers():
    idle_workers = Worker.objects.filter(status='idle')
    for worker in idle_workers:
        print('Terminate Worker')
        AWS().terminate(worker.worker_id)
        print('Terminate Worker', worker.id)
        worker.status = 'terminated'
        worker.save()

@app.task(queue="master")
def terminate_worker(worker_id):
    worker = Worker.objects.get(id=worker_id)
    
    print('Terminate Worker', worker.id)
    AWS().terminate(worker.worker_id)
    worker.status = 'terminated'
    worker.save()

@app.task(queue="master")
def install_worker(worker_id):
    worker = Worker.objects.get(id=worker_id)
    print('Install Worker', worker.id)
    if settings.DEFAULT_PROVIDER == 'AWS':
        AWS().install(worker.ip)

@app.task(queue="master")
def update_worker(worker_id):
    worker = Worker.objects.get(id=worker_id)
    print('Update Worker', worker.id)
    if settings.DEFAULT_PROVIDER == 'AWS':
        AWS().update(worker.ip)

    # command = 'rsync -avz {} root@%s:/projects/mendelmd'.format(settings.BASE_DIR, worker.ip)

@app.task(queue="master")
def check_workers():

    workers = Worker.objects.all()
    for worker in workers:

        ip = worker.ip
        # print(worker.status)
        # command = """top -b -n 10 -d.2 | grep 'Cpu' |  awk 'NR==3{ print($2)}'"""
        # command = 'top -b -n 1 | head -n 10'
        command = 'top -bcn1 -w512 | head -n 10'
        
        command = """ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ubuntu@%s %s""" % (ip,command)
        output = check_output(command, shell=True)
        # print(output.decode('utf-8'))
        text = output.decode('utf-8').splitlines()

        process_list_started = False
        for line in text:
            # print(line)
            if line.startswith('%Cpu(s)'):
                cpu_usage = line.split()[0]

            if process_list_started:
                process = line
                break

            if line.startswith('  PID USER'):
                process_list_started = True
            
        # print(process.split())
        rows = process.split()
        current_process = ' '.join(rows[10:])
        output = '{} {}'.format(cpu_usage, current_process)
        # print(output)
        worker.current_status = output
        worker.save()