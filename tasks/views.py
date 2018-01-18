from django.shortcuts import render
from .models import Task
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from tasks.tasks import check_file, download_file


@login_required
def index(request):

    if request.user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(user=request.user)

    context = {
        'tasks':tasks,
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


@login_required
def run_task(request, task_id):

    if request.user.is_staff:
        task = Task.objects.get(pk=task_id)
    else:
        task = Task.objects.get(pk=task_id, user=request.user)

    if task.action == "check":
        check_file.delay(task.id)
    if task.action == "download":
        download_file.delay(task.id)

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
            
                if task.action == "check":
                    task.status = 'scheduled'
                    check_file.delay(task.id)
                if task.action == "download":
                    task.status = 'scheduled'
                    download_file.delay(task.id)
                task.save()

            if action == "delete":
                task.delete()

    return redirect('tasks-index')
