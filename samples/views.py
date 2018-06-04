from django.shortcuts import render

from .models import Sample, SampleGroup
from files.models import File
from tasks.models import Task
import json
from tasks.tasks import annotate_vcf, run_qc

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

from files.tasks import import_vcf

# from sample_tracking_system.users.models import User
from django.contrib.auth.models import User

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import F, Count

from django.contrib.auth.decorators import login_required
import csv

from django.http import HttpResponseRedirect, HttpResponse

import io

from samples.forms import SampleGroupForm

from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from django.contrib import messages


# Create your views here.
@login_required
def index(request):

    args = []

    if request.method == 'POST':
        action = request.POST['action']
        samples = request.POST.getlist('samples')
        # print('samples', samples)
        request.session['samples'] = samples
        return redirect('create_group')

    else:

        samples = Sample.objects.filter(*args).order_by('id')

    context = {
        'samples':samples,
    }

    return render(request, 'samples/index.html', context)


@login_required
def create_group(request):
    if request.method == 'POST':

        form = SampleGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sample_index')
    else:
        samples = request.session['samples']
        print('samples', samples)
        form = SampleGroupForm(initial = {'members': [1,2,3] })
        # form.members.initial = ['537']
    return render(request, 'samples/create_group.html', {'form': form})


def group_detail(request, pk):
    object = SampleGroup.objects.get(pk=pk)
    n_samples = object.members.count()

    context = {
        'object':object,
        'n_samples':n_samples
    }
    return render(request, 'samples/samplegroup_detail.html', context)

class SampleGroupList(ListView):
    model = SampleGroup


class SampleGroupDelete(DeleteView):
    model = SampleGroup
    success_url = reverse_lazy('samplegroup-list')

class SampleDetailView(DetailView):
    model = Sample

class SampleGroupUpdateView(UpdateView):
    model = SampleGroup
    fields = '__all__'

def sample_import_vcf(request, pk):
    sample = Sample.objects.get(pk=pk)
    messages.add_message(request, messages.SUCCESS, 'VCF from sample {} will be imported'.format(sample.name))
    import_vcf.delay(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def bulk_action(request):

    if request.method == 'POST':
        samples = request.POST.getlist('samples')
        action = request.POST['action']
        print(action, samples)
        for sample_id in samples:
            if action == "import_vcf":
                import_vcf.apply_async(sample_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
