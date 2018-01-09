from django.shortcuts import render
from .models import Task
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from tasks.tasks import check_file, download_file



def index(request):

    tasks = Task.objects.all()
    context = {
        'tasks':tasks,
    }
    return render(request, 'tasks/index.html', context)

class TaskDelete(DeleteView):
    model = Task
    # template_name = "email_delete.html"
    success_url = reverse_lazy('tasks-index')

    # def delete(self, request, *args, **kwargs):
    #    self.object = self.get_object()
    #    if self.object.user == request.user:
    #       self.object.delete()
    #       return HttpResponseRedirect(self.get_success_url())
    #    else:
    #       raise Http404 #or return HttpResponse('404_url')


def run_task(request, task_id):
    task = Task.objects.get(pk=task_id)

    if task.action == "check":
        check_file.delay(task.id)
    if task.action == "download":
        download_file.delay(task.id)

    task.status = 'scheduled'
    task.save()

    return redirect('tasks-view', task.id)


class TaskDetail(DetailView):

    model = Task

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['book_list'] = Book.objects.all()
    #     return context


@login_required
def bulk_action(request):
    if request.method == 'POST':
        tasks = request.POST.getlist('tasks')
        action = request.POST['action']
        
        for task_id in tasks:

            task = Task.objects.get(pk=task_id)
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
