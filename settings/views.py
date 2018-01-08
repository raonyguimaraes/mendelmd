from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.shortcuts import render
from .models import S3Credential
from .forms import S3CredentialForm

from django.urls import reverse_lazy

# Create your views here.
def index(request):
    s3_settings = S3Credential.objects.all()
    context = {'s3_settings':s3_settings}
    return render(request, 'settings/index.html', context)


def create_s3_credential(request):
    form = S3CredentialForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            s3credential = S3Credential(user=request.user)
            s3credential.name = form.cleaned_data['name']
            s3credential.access_key = form.cleaned_data['access_key']
            s3credential.secret_key = form.cleaned_data['secret_key']
            s3credential.buckets = form.cleaned_data['buckets']
            s3credential.exclude_paths = form.cleaned_data['exclude_paths']
            s3credential.exclude_files = form.cleaned_data['exclude_files']
            s3credential.save()
            return redirect('settings-index')
    context = {'form': form}
    return render(request, 'settings/create-s3-credential.html', context)

class S3CredentialUpdate(UpdateView):
    model = S3Credential
    fields = ['name', 'access_key', 'secret_key', 'buckets', 'exclude_paths', 'exclude_files']

def settings_s3_view(request, settings_s3_id):
    print('Hello')


class S3CredentialDelete(DeleteView):
    model = S3Credential
    success_url = reverse_lazy('settings-index')
