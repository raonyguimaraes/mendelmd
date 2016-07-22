from django.conf import settings
from django.conf.urls import *
from django.conf.urls import patterns, url, include

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import admin
from diseases.views import DiseaseListView
from diseases.models import Disease

admin.autodiscover()

urlpatterns = patterns("",
    url(r"^populate/$", 'diseases.views.populate', name="diseases_populate"),
    url(r"^populate_genes/$", 'diseases.views.populate_genes', name="populate_genes"),

    url(r"^populate_hgmd_genes/$", 'diseases.views.populate_hgmd_genes', name="populate_hgmd_genes"),
    url(r"^populate_hgmd_mutations/$", 'diseases.views.populate_hgmd_mutations', name="populate_hgmd_mutations"),
    
    #url(r"^$", 'diseases.views.list', name="diseases_list"),
    
    url(r'^$', DiseaseListView.as_view(model=Disease), name="diseases_list"),
    

    
    url(r'^view/(?P<disease_id>\d+)/$', 'diseases.views.view', name='disease_view'),
    )