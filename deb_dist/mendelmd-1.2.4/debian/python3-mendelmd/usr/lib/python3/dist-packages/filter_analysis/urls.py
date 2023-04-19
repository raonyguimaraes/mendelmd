from django.conf.urls import *
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from filter_analysis.models import *

from filter_analysis.views import FilterAnalysisUpdateView, FilterAnalysisDeleteView, FilterConfigUpdateView, FilterConfigDeleteView

from filter_analysis import views

urlpatterns = [

    url(r'^$', views.index, name='filter_analysis'),
    url(r'^table/$', views.filter_analysis_table, name='filter_analysis_table'),
    url(r'^family_analysis/$', views.family_analysis, name='family_analysis'),
    url(r'^family_analysis/create/$', views.family_analysis_create_filter, name='family_analysis_create_filter'),  
    url(r'^wizard/$', views.wizard, name='filter_wizard'),
    url(r'^oneclick/$', views.oneclick, name='oneclick'),
    url(r'^test/$', views.test, name='test'),    
    url(r'^create/$', views.create, name='create_filter'),
    url(r'^createconfig/$', views.createconfig, name='create_config'),
    url(r'^updateanalysis/(?P<pk>\d+)', FilterAnalysisUpdateView.as_view(model=FilterAnalysis), name="analysis_update",),
    url(r'^deleteanalysis/(?P<pk>\d+)', FilterAnalysisDeleteView.as_view(), name="analysis_delete",),
    url(r'^updateconfig/(?P<pk>\d+)', FilterConfigUpdateView.as_view(model=FilterConfig), name="config_update",),
    url(r'^deleteconfig/(?P<pk>\d+)', FilterConfigDeleteView.as_view(), name="config_delete",),
]
