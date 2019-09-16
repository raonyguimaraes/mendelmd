from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
#from filter_analysis.models import *
#from filter_analysis.views import FilterAnalysisUpdateView, FilterAnalysisDeleteView, FilterConfigUpdateView, FilterConfigDeleteView

urlpatterns = patterns('pathway_analysis.views',
    url(r'^$', 'index', name='pathway_analysis'),
    url(r'^populate/$', 'populate', name='populate_pathway'),
    url(r'^analysis/$', 'analysis', name='pathway_filter_analysis'),
    url(r'^view/(?P<pathway_id>\d+\w+)$', 'view', name='pathway_view'),
    
#    url(r'^trioanalysis/$', 'trioanalysis', name='trio_analysis'),
#    
#    
#    
#    url(r'^wizard/$', 'wizard', name='filter_wizard'),
##    url(r'^create/$', 'create', name='create_filter'),
#    url(r'^create/$', 'create', name='create_filter'),
#    url(r'^createconfig/$', 'createconfig', name='create_config'),
#    url(r'^updateanalysis/(?P<pk>\d+)', FilterAnalysisUpdateView.as_view(model=FilterAnalysis), name="analysis_update",),
#    url(r'^deleteanalysis/(?P<pk>\d+)', FilterAnalysisDeleteView.as_view(), name="analysis_delete",),
#    url(r'^updateconfig/(?P<pk>\d+)', FilterConfigUpdateView.as_view(model=FilterConfig), name="config_update",),
#    url(r'^deleteconfig/(?P<pk>\d+)', FilterConfigDeleteView.as_view(), name="config_delete",),
)
