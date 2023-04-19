from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib import messages

from workers.models import Worker
from workers.tasks import launch_worker, launch_workers, terminate_worker, install_worker, check_workers, update_worker

from subprocess import check_output, call

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required
def index(request):
    workers = Worker.objects.all().order_by('-id')
    context = {'workers':workers}
    return render(request, 'workers/index.html', context)

@login_required
def launch(request):
    n = request.GET.get('n')
    if n:
        for i in range(0,int(n)):
            launch_worker.delay()
    else:
        launch_worker.delay()
    messages.success(request, 'Worker is being launched.')
    return redirect('worker-list')

@login_required
def terminate(request, pk):
    worker=Worker.objects.get(pk=pk)
    terminate_worker.delay(worker.id)
    messages.success(request, 'Worker is being terminated.')
    return redirect('worker-list')

@login_required
def install(request, pk):
    worker=Worker.objects.get(pk=pk)
    install_worker.delay(worker.id)
    messages.success(request, 'Worker is being installed.')
    return redirect('worker-list')

@login_required
def update(request, pk):
    worker=Worker.objects.get(pk=pk)
    update_worker.delay(worker.id)
    messages.success(request, 'Worker is being updated!')
    return redirect('worker-list')

class WorkerDelete(LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy('worker-list')


def action(request):
    if request.method == 'POST':
        print('Hello World')
        action = request.POST['action']
        workers = request.POST.getlist('select[]')
        
        # print(action, workers)
        for worker_id in workers:
            
            worker=Worker.objects.get(id=worker_id)

            if action == 'run':
                worker.current_status = 'queued'
                worker.save()
            elif action == 'update':
                update_worker.delay(worker.id)
            elif action == 'install':
                install_worker.delay(worker.id)
                worker.status = 'installing'
                worker.save()
            elif action == 'terminate':
                terminate_worker.delay(worker.id)
                worker.status = 'will be terminated'
                worker.save()
            elif action == 'delete':
                worker.delete()
        
        if action == 'check':                
            check_workers.delay()
            
                
    return redirect('worker-list')    