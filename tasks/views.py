from django.shortcuts import render

from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from tasks.models import Task

# Create your views here.
def index(request):
    print('hello world!')
    tasks = Task.objects.all()
    context = {'tasks':tasks}
    return render(request, 'tasks/index.html', context)
def run(request, task_id):
    print('Hello')
def edit(request, task_id):
    print('Hello')
def delete(request, task_id):
    print('Hello')

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('task-index')
