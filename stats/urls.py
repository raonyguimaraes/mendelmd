from django.conf import settings
from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

from . import views

from django.urls import include, path

urlpatterns = [
    path('', views.index, name="statistics_index"),
]