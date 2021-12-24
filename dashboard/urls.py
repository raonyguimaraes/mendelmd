from django.urls import include, path
from . import views

urlpatterns = [
    path(r'', views.index, name='dashboard'),
    path(r'^bulk_action', views.bulk_action, name='bulk_action'),
]