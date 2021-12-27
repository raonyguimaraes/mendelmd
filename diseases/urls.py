from django.conf import settings
from django.urls import include, path

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import admin
from diseases.views import DiseaseListView
from diseases.models import Disease

admin.autodiscover()

from . import views

from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    path(r"populate/", views.populate, name="diseases_populate"),
    path(r"populate_genes/", views.populate_genes, name="populate_genes"),

    path(r"populate_hgmd_genes/", views.populate_hgmd_genes, name="populate_hgmd_genes"),
    path(r"populate_hgmd_mutations/", views.populate_hgmd_mutations, name="populate_hgmd_mutations"),
    
    #path(r"", 'diseases.views.list', name="diseases_list"),
    
    path(r'', login_required(DiseaseListView.as_view(model=Disease)), name="diseases_list"),
    

    
    path(r'view/(?P<disease_id>\d+)/', views.view, name='disease_view'),
    ]