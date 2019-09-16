# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
from django.core.paginator import Paginator
from .models import Dbnfsp, Genome1kVariant, Genome1kSample, Genome1kGenotype, Genome1kSampleVariant, Genome1kVariantIndex
from .forms import Genomes1kForm
from datetime import datetime


@login_required
def index(request):

    return render(request, 'databases/index.html')


def dbnfsp_index(request):

    dbnfsp_list = Dbnfsp.objects.first()
    # paginator = Paginator(dbnfsp_list, 25)

    context = {'dbnfsp_list':dbnfsp_list}

    return render(request, 'dbnfsp/index.html', context)    

def genomes1k_index(request):

    start = datetime.now()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Genomes1kForm(request.POST)
        if form.is_valid():
            sample = form.cleaned_data['sample']
            genomes1k_variants = Genome1kSampleVariant.objects.filter(sample__name=sample, genotype__genotype='1|1')
            query_variants = genomes1k_variants.count()
            # query_variants = 0
            # len(genomes1k_variants)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Genomes1kForm()
        genomes1k_variants = Genome1kSampleVariant.objects.all()[:10]
        query_variants = 0#genomes1k_variants.count()
    
    total_variants = Genome1kSampleVariant.objects.all().count()
    # total_variants = 0

    # for item in genomes1k_variants:
    #   print(dir(item))
    # paginator = Paginator(dbnfsp_list, 25)

    end = datetime.now()
    time_taken = end-start


    context = {
    'genomes1k_variants':genomes1k_variants,
    'total_variants':total_variants,
    'query_variants':query_variants,
    'time_taken':time_taken,
    'form':form
    }


    return render(request, '1000genomes/index.html', context)   