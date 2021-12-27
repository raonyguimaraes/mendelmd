from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from filter_analysis.models import *

from filter_analysis.views import FilterAnalysisUpdateView, FilterAnalysisDeleteView, FilterConfigUpdateView, FilterConfigDeleteView

from filter_analysis import views
from django.urls import include, path


urlpatterns = [

    path('', views.index, name='filter_analysis'),
    path('table/', views.filter_analysis_table, name='filter_analysis_table'),
    path('family_analysis/', views.family_analysis, name='family_analysis'),
    path('family_analysis/create/', views.family_analysis_create_filter, name='family_analysis_create_filter'),
    path('wizard/', views.wizard, name='filter_wizard'),
    path('oneclick/', views.oneclick, name='oneclick'),
    path('test/', views.test, name='test'),
    path('create/', views.create, name='create_filter'),
    path('createconfig/', views.createconfig, name='create_config'),
    path('updateanalysis/<int:pk>', FilterAnalysisUpdateView.as_view(model=FilterAnalysis), name="analysis_update",),
    path('deleteanalysis/<int:pk>', FilterAnalysisDeleteView.as_view(), name="analysis_delete",),
    path('updateconfig/<int:pk>', FilterConfigUpdateView.as_view(model=FilterConfig), name="config_update",),
    path('deleteconfig/<int:pk>', FilterConfigDeleteView.as_view(), name="config_delete",),
]
