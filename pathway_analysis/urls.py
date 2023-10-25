
from django.urls import include, path

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
#from filter_analysis.models import *
#from filter_analysis.views import FilterAnalysisUpdateView, FilterAnalysisDeleteView, FilterConfigUpdateView, FilterConfigDeleteView

from . import views


urlpatterns = [
    path("", views.index, name='pathway_analysis'),
    path("populate", views.populate, name='populate_pathway'),
    path("analysis/", views.analysis, name='pathway_filter_analysis'),
    path("view/<str:pathway_id>/", views.view, name='pathway_view'),
    ]
    
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

