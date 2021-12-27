from django.conf import settings
from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

from . import views
from django.urls import include, path


urlpatterns = [
    path(r"^$", views.index, name="statistics_index"),    
]