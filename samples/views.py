from django.shortcuts import render

from .models import Sample, SampleGroup
from files.models import File
from tasks.models import Task
import json
from tasks.tasks import annotate_vcf, run_qc

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

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



class SampleGroupList(ListView):
    model = SampleGroup


class SampleGroupDelete(DeleteView):
    model = SampleGroup
    success_url = reverse_lazy('samplegroup-list')