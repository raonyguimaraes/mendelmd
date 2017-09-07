from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from tasks.models import Task
from tasks.tasks import annotate_vcf, insert_vcf


# Create your views here.
def index(request):
    print('hello world!')
    tasks = Task.objects.all()
    context = {'tasks':tasks}
    return render(request, 'tasks/index.html', context)

def run(request, task_id):
    print('Hello Run')
    task=Task.objects.get(id=task_id)
    task.status = 'new'
    task.save()
    annotate_vcf.delay(task.id)
    messages.success(request, 'Task will run soon.')
    return redirect('task-index')

def annotate(request, task_id):
    print('Hello Annotate')
    task=Task.objects.get(id=task_id)
    annotate_vcf.delay(task.id)
    messages.success(request, 'Task will run soon.')
    return redirect('task-index')

def insert(request, task_id):
    print('Hello Insert')
    task=Task.objects.get(pk=task_id)
    insert_vcf.delay(task.id)
    messages.success(request, 'Task will run soon.')
    return redirect('task-index')


def edit(request, task_id):
    print('Hello')
def delete(request, task_id):
    print('Hello')

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('task-index')
