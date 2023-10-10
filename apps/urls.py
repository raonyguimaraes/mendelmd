from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="webapps_index"),   
    path("import", views.import_apps, name="import_apps"), 
]
