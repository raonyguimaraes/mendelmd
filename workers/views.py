from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib import messages

from workers.models import Worker
from workers.tasks import launch_workers, terminate_worker, install_worker

# Create your views here.
def index(request):
    workers = Worker.objects.all()
    context = {'workers':workers}
    return render(request, 'workers/index.html', context)

def launch(request):
    launch_workers.delay(1)
    messages.success(request, 'Worker is being launched.')
    return redirect('worker-list')

def terminate(request, pk):
    worker=Worker.objects.get(pk=pk)
    terminate_worker.delay(worker.id)
    messages.success(request, 'Worker is being terminated.')
    return redirect('worker-list')

def install(request, pk):
    worker=Worker.objects.get(pk=pk)
    install_worker.delay(worker.id)
    messages.success(request, 'Worker is being installed.')
    return redirect('worker-list')


class WorkerDelete(DeleteView):
    model = Worker
    success_url = reverse_lazy('worker-list')