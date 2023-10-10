from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("import_from_hetzner", views.import_from_hetzner, name="import_from_hetzner"),
]
