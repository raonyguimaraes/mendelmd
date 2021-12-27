from django.conf.urls import *

from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='variant_index'),
    path('view/<int:variant_id>/', views.view, name='variant_view'),
]