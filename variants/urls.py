from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="variant_index"),
    path("view/<int:variant_id>/", views.view, name="variant_view"),
    
]