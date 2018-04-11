from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from .models import S3Credential, Provider, Profile
from .forms import S3CredentialForm

from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@login_required
def index(request):

    if request.user.is_staff:
        s3_settings = S3Credential.objects.all()
    else:
        s3_settings = S3Credential.objects.filter(user=request.user)

    context = {'s3_settings':s3_settings}
    return render(request, 'settings/index.html', context)

@login_required
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

class S3CredentialUpdate(LoginRequiredMixin, UpdateView):
    model = S3Credential
    fields = ['name', 'access_key', 'secret_key', 'buckets', 'exclude_paths', 'exclude_files']

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects


@method_decorator(login_required, name='dispatch')
class S3CredentialDetailView(DetailView):
    model = S3Credential
    # def get_queryset(self):
    #     return self.model.objects.filter(user=self.request.user)
    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects

@method_decorator(login_required, name='dispatch')
class S3CredentialDelete(DeleteView):
    model = S3Credential
    success_url = reverse_lazy('settings-index')
    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects

class ProviderCreate(CreateView):
    model = Provider
    fields = ['name', ]
