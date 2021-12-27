from django.conf import settings

from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.index, name="databases_index"),
    path('dbnfsp/', views.dbnfsp_index, name="dbnfsp_index"),
    path('1000genomes/', views.genomes1k_index, name="1000genomes_index"),
]