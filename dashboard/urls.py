from django.urls import include, path

from . import views
urlpatterns = [
    path("", views.index, name="dashboard"),
    path("apps/", views.apps, name="dashboard-apps"),
    path("bulk_action/", views.bulk_action, name="bulk_action"),
]