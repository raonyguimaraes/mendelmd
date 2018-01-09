from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.management import call_command

from .models import File#, S3Credential


# Create your views here.
def index(request):
    files = File.objects.all()
    context = {'files':files}
    return render(request, 'files/index.html', context)

def view(request, file_id):
    print('Hello')


#crud for s3 settings
def settings_index(request):
    s3_settings = S3Credential.objects.all()
    context = {'s3_settings':s3_settings}
    return render(request, 'files/settings/index.html', context)


def settings_view(request, settings_id):
    print('Hello')




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