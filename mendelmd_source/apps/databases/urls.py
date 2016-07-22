from django.conf import settings
from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^$", 'databases.views.index', name="databases_index"),
    
    )