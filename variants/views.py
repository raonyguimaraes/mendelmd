from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from collections import OrderedDict as SortedDict
from variants.models import *

import pickle
import json

@login_required
def index(request):
    variants = Variant.objects.all()[:10]
    context = {'variants':variants}
    return render(request, 'variants/index.html', context)

@login_required
def view(request, variant_id):
    variant = get_object_or_404(Variant, pk=variant_id)

    variant.info = json.loads(variant.info)

    new_dict = SortedDict()
    key_list = list(variant.info.keys())
    key_list.sort()
    for key in key_list:
        new_dict[key] = variant.info[key]

    variant.info = new_dict
    print(type(variant.info))

    return render(request, 'variants/view.html', {'variant': variant})
