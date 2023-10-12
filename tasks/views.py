import os
import select
import subprocess
import sys
from subprocess import check_output

import paramiko
from django.shortcuts import render
from .models import Task
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from tasks.tasks import task_run_task
from files.tasks import check_file
from django.db.models import Q
from collections import Counter
from files.models import File
import time

@login_required
def index(request):

    query = request.GET.get('query', '')
    args = []

    if query != '':
        args.append(Q(name__icontains=query))

    if request.user.is_staff:
        tasks = Task.objects.filter(*args).order_by('-id')
    else:
        tasks = Task.objects.filter(*args, user=request.user).order_by('-id')

    tasks_summary = dict(Counter(tasks.values_list('status', flat=True)))
    n_tasks = len(tasks) 

    context = {
        'tasks':tasks,
        'n_tasks':n_tasks,
        'tasks_summary':tasks_summary
    }
    return render(request, 'tasks/index.html', context)

@method_decorator(login_required, name='dispatch')
class TaskDelete(DeleteView):

    model = Task

    success_url = reverse_lazy('tasks-index')
    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects
def run_remote_command(ip,command):
    command = """ssh -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@{} '{} </dev/null'""".format(
        ip,command)
    print('remote',command)
    try:
        output = check_output(command, shell=True,stderr=subprocess.STDOUT).decode()
        print(output)
    except subprocess.CalledProcessError as e:
        print(e)
        print(e.stdout.decode())
        # output=e.stdout
        output=str(e.stdout.decode())

    return(output)

def run_local_command(command):
    print('local',command)
    try:
        output = check_output(command, shell=True,stderr=subprocess.STDOUT).decode()
        print(output)
    except subprocess.CalledProcessError as e:
        print(e)
        print(e.stdout.decode())
        # output=e.stdout
        output=str(e.stdout.decode())
    # f = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # p = select.poll()
    # p.register(f.stdout)

    # while True:
    #     if p.poll(1):
    #         print(f.stdout.readline().decode())
    #     time.sleep(1)

    return(output)

class TransferApp:
    def __init__(self,task):
        self.task_id=task.id
        self.data=task.manifest

    def transfer(self):
        print('Lets transfer this app now!')
        data=self.data
        print(data)
        

        if data['task_type']=='transfer_nf-tower_local':
            print('transfer_nf-tower_lxd')
            original_wd=os.getcwd()
            #create workdir
            # os.chdir('work_dir/')
            # print(os.getcwd())
            ip_origin=data['server_ip']
            ip_dest = data['server_destination']
            command = 'bash scripts/transfer_nf-tower_to_lxd.sh {} {} > work_dir/out.{}.log 2>&1 &'.format(ip_origin,ip_dest,self.task_id)#
            run_local_command(command)


@login_required
def run_task(request, task_id):

    if request.user.is_staff:
        task = Task.objects.get(pk=task_id)
    else:
        task = Task.objects.get(pk=task_id, user=request.user)

    task.output=TransferApp(task).transfer()
    #task_run_task.delay(task.id)

    # if task.action == "check":
    #     check_file.delay(task.id)
    # if task.action == "download":
    #     download_file.delay(task.id)

    task.status = 'scheduled'
    task.save()

    return redirect('tasks-view', task.id)

@method_decorator(login_required, name='dispatch')
class TaskDetail(DetailView):
    model = Task
    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # files = self.object.manifest['files']
        context['output'] = open('work_dir/out.{}.log'.format(self.object.id)).read()
        context['output_lines']=len(context['output'].splitlines())
        command = 'tail work_dir/out.{}.log'.format(self.object.id)
        out=check_output(command,shell=True).decode()
        context['output_tail'] = out

        # context['input_files'] = File.objects.filter(pk__in=files)
        # context['output_files'] = File.objects.filter(task=self.object.id)
        return context
        
@login_required
def bulk_action(request):
    if request.method == 'POST':
        
        tasks = request.POST.getlist('tasks')
        action = request.POST['action']
        
        for task_id in tasks:

            if request.user.is_staff:
                task = Task.objects.get(pk=task_id)
            else:
                task = Task.objects.get(pk=task_id, user=request.user)
            
            #save to change modified date
            task.save()

            if action == "run":
                
                task_run_task.delay(task.id)
                # if task.action == "qc":
                #     task.status = 'scheduled'
                #     run_qc.delay(task.id)
                # if task.action == "check":
                #     task.status = 'scheduled'
                #     check_file.delay(task.id)
                # if task.action == "download":
                #     task.status = 'scheduled'
                #     download_file.delay(task.id)
                task.status = 'scheduled'
                task.save()

            if action == "delete":
                task.delete()

    return redirect('tasks-index')
