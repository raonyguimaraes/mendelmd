from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from filter_analysis.models import *

from filter_analysis.views import FilterAnalysisUpdateView, FilterAnalysisDeleteView, FilterConfigUpdateView, FilterConfigDeleteView

from filter_analysis import views
from django.urls import include, path


urlpatterns = [

    path(r'', views.index, name='filter_analysis'),
    path(r'table/', views.filter_analysis_table, name='filter_analysis_table'),
    path(r'family_analysis/', views.family_analysis, name='family_analysis'),
    path(r'family_analysis/create/', views.family_analysis_create_filter, name='family_analysis_create_filter'),  
    path(r'wizard/', views.wizard, name='filter_wizard'),
    path(r'oneclick/', views.oneclick, name='oneclick'),
    path(r'test/', views.test, name='test'),    
    path(r'create/', views.create, name='create_filter'),
    path(r'createconfig/', views.createconfig, name='create_config'),
    path(r'updateanalysis/(?P<pk>\d+)', FilterAnalysisUpdateView.as_view(model=FilterAnalysis), name="analysis_update",),
    path(r'deleteanalysis/(?P<pk>\d+)', FilterAnalysisDeleteView.as_view(), name="analysis_delete",),
    path(r'updateconfig/(?P<pk>\d+)', FilterConfigUpdateView.as_view(model=FilterConfig), name="config_update",),
    path(r'deleteconfig/(?P<pk>\d+)', FilterConfigDeleteView.as_view(), name="config_delete",),
]
