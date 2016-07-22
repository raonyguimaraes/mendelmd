from django.conf import settings
from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^$", 'statistics.views.index', name="statistics_index"),
    
    )