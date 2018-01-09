from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.management import call_command

from .models import File
from django.contrib.auth.decorators import login_required

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

@login_required
class FileUpdate(UpdateView):
    model = File
    fields = '__all__'

@login_required
class FileDelete(DeleteView):
    model = File
    success_url = reverse_lazy('files-index')