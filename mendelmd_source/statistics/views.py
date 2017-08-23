# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

from variants.models import *
from individuals.models import *
from genes.models import Gene as Gene2
from diseases.models import *


import collections

@login_required
def index(request):

    statistics = collections.OrderedDict()

    statistics['Individuals'] = Individual.objects.all().count()
    statistics['Variants'] = Variant.objects.all().count()
    statistics['Genes'] = Gene2.objects.all().count()
    statistics['Diseases'] = Disease.objects.all().count()
    statistics['Diseases Genes'] = Gene.objects.all().count()
    # return render_to_response('statistics/index.html', context_instance=RequestContext(request))
    return render(request, 'statistics/index.html', {"statistics": statistics})
