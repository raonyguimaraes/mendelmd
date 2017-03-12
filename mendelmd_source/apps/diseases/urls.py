from django.conf import settings
from django.conf.urls import *

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import admin
from diseases.views import DiseaseListView
from diseases.models import Disease

admin.autodiscover()

from . import views

from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r"^populate/$", views.populate, name="diseases_populate"),
    url(r"^populate_genes/$", views.populate_genes, name="populate_genes"),

    url(r"^populate_hgmd_genes/$", views.populate_hgmd_genes, name="populate_hgmd_genes"),
    url(r"^populate_hgmd_mutations/$", views.populate_hgmd_mutations, name="populate_hgmd_mutations"),
    
    #url(r"^$", 'diseases.views.list', name="diseases_list"),
    
    url(r'^$', login_required(DiseaseListView.as_view(model=Disease)), name="diseases_list"),
    

    
    url(r'^view/(?P<disease_id>\d+)/$', views.view, name='disease_view'),
    ]