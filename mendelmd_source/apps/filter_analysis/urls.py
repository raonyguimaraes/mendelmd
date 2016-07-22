from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from filter_analysis.models import *

from filter_analysis.views import FilterAnalysisUpdateView, FilterAnalysisDeleteView, FilterConfigUpdateView, FilterConfigDeleteView

urlpatterns = patterns('filter_analysis.views',
    url(r'^$', 'index', name='filter_analysis'),

    url(r'^table/$', 'filter_analysis_table', name='filter_analysis_table'),


    url(r'^family_analysis/$', 'family_analysis', name='family_analysis'),
    
    url(r'^family_analysis/create/$', 'family_analysis_create_filter', name='family_analysis_create_filter'),  
    
    url(r'^wizard/$', 'wizard', name='filter_wizard'),
    url(r'^oneclick/$', 'oneclick', name='oneclick'),
    
#    url(r'^create/$', 'create', name='create_filter'),
    url(r'^create/$', 'create', name='create_filter'),
    url(r'^createconfig/$', 'createconfig', name='create_config'),
    url(r'^updateanalysis/(?P<pk>\d+)', FilterAnalysisUpdateView.as_view(model=FilterAnalysis), name="analysis_update",),
    url(r'^deleteanalysis/(?P<pk>\d+)', FilterAnalysisDeleteView.as_view(), name="analysis_delete",),
    url(r'^updateconfig/(?P<pk>\d+)', FilterConfigUpdateView.as_view(model=FilterConfig), name="config_update",),
    url(r'^deleteconfig/(?P<pk>\d+)', FilterConfigDeleteView.as_view(), name="config_delete",),
)
