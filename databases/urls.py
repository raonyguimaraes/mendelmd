from django.conf import settings

from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = [
    url(r"^$", views.index, name="databases_index"),
    url(r"^dbnfsp/$", views.dbnfsp_index, name="dbnfsp_index"),
    url(r"^1000genomes/$", views.genomes1k_index, name="1000genomes_index"),
]