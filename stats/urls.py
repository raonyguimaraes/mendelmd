# from django.conf import settings
# from django.conf.urls import *
from django.urls import include, path

# from django.contrib import admin
# admin.autodiscover()

from . import views

urlpatterns = [
        path("", views.index, name="statistics_index"),
]