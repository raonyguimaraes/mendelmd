from django.urls import include, path
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from . import views
from django.urls import path

from .forms import ContactForm1, ContactForm2
from .views import ContactWizard

urlpatterns = [
    path("", views.index, name="analyses-index"),
    # path("create/", views.AnalysisCreate.as_view(), {}, "analysis-create"),
    path("create/", views.create, {}, "analysis-create"),
    path("detail/<int:pk>/", views.AnalysisDetailView.as_view(), name="analysis-detail"),
    path("delete/<int:pk>/", views.AnalysisDelete.as_view(), name="analysis-delete"),
    path("update/<int:pk>/", views.AnalysisUpdate.as_view(), name="analysis-update"),
    path("run/<int:analysis_id>/", views.run_analysis, name="analysis-run"),
    path("contact/", ContactWizard.as_view([ContactForm1, ContactForm2])),
]