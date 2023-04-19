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
    path('populate/', views.populate, name='diseases_populate'),
    path('populate_genes/', views.populate_genes, name='populate_genes'),

    path('populate_hgmd_genes/', views.populate_hgmd_genes, name='populate_hgmd_genes'),
    path('populate_hgmd_mutations/', views.populate_hgmd_mutations, name='populate_hgmd_mutations'),
    
    #path('', 'diseases.views.list', name='diseases_list'),
    
    path('', login_required(DiseaseListView.as_view(model=Disease)), name='diseases_list'),
    

    
    path('view/<int:disease_id>/', views.view, name='disease_view'),
    ]