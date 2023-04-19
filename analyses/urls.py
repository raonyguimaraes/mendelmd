from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from . import views

from .forms import ContactForm1, ContactForm2
from .views import ContactWizard
from django.urls import include, path


urlpatterns = [
    path(r'', views.index, name='analyses-index'),
    # path(r'create/', views.AnalysisCreate.as_view(), {}, 'analysis-create'),
    path(r'create/', views.create, {}, 'analysis-create'),
    path(r'detail/<int:pk>/', views.AnalysisDetailView.as_view(), name='analysis-detail'),
    path(r'delete/<int:pk>/', views.AnalysisDelete.as_view(), name='analysis-delete'),
    path(r'update/<int:pk>/', views.AnalysisUpdate.as_view(), name='analysis-update'),
    path(r'run/<int:analysis_id>/', views.run_analysis, name='analysis-run'),
    path(r'contact/', ContactWizard.as_view([ContactForm1, ContactForm2])),
]