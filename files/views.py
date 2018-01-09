from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.management import call_command

from files.models import File
from django.contrib.auth.decorators import login_required

from tasks.tasks import check_file
from tasks.models import Task

@login_required
def index(request):

    if request.user.is_staff:
        files = File.objects.all()
    else:
        files = File.objects.filter(user=request.user)

    context = {'files':files}
    return render(request, 'files/index.html', context)

@login_required
def view(request, file_id):
    print('Hello')

@login_required
def settings_index(request):
    s3_settings = S3Credential.objects.all()
    context = {'s3_settings':s3_settings}
    return render(request, 'files/settings/index.html', context)

@login_required
def settings_view(request, settings_id):
    print('Hello')


@login_required
def import_files(request):
    print('Hello World')
    call_command('import_files')
    return redirect('files-index')

class FileUpdate(UpdateView):
    model = File
    fields = '__all__'

class FileDelete(DeleteView):
    model = File
    success_url = reverse_lazy('files-index')


@login_required
def bulk_action(request):
    if request.method == 'POST':
        files = request.POST.getlist('files')
        action = request.POST['action']

        for file_id in files:
            file = File.objects.get(pk=file_id)
            
            if action == "delete":
                file.delete()
            if action == "check":
                
                task_manifest = {}
                task_manifest['file'] = file.id
                task_manifest['action'] = action
                task = Task(user=request.user)
                
                task.manifest = task_manifest
                task.status = 'new'
                task.action = action
                task.user = request.user
                task.save()

                check_file.delay(task.id)

                file.status = 'scheduled'
                file.save()

    return redirect('files-index')
