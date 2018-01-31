from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from . import views
from django.urls import path

from .forms import ContactForm1, ContactForm2
from .views import ContactWizard

urlpatterns = [
    url(r'^$', views.index, name='analyses-index'),
    # url(r'^create/$', views.AnalysisCreate.as_view(), {}, 'analysis-create'),
    url(r'^create/$', views.create, {}, 'analysis-create'),
    url(r'detail/(?P<pk>\d+)/$', views.AnalysisDetailView.as_view(), name='analysis-detail'),
    url(r'delete/(?P<pk>\d+)/$', views.AnalysisDelete.as_view(), name='analysis-delete'),
    url(r'update/(?P<pk>\d+)/$', views.AnalysisUpdate.as_view(), name='analysis-update'),
    url(r'run/(?P<analysis_id>\d+)/$', views.run_analysis, name='analysis-run'),
    url(r'^contact/$', ContactWizard.as_view([ContactForm1, ContactForm2])),
]