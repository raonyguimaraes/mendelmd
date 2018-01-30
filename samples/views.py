from django.shortcuts import render

from .models import Sample
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

# Create your views here.
@login_required
def index(request):

    args = []

    samples = Sample.objects.filter(*args).order_by('id')

    context = {
        'samples':samples,
    }

    return render(request, 'samples/index.html', context)
