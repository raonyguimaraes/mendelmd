from django.conf.urls import *

from . import views
from django.urls import include, path

urlpatterns = [
    path(r'^$', views.index, name='variant_index'),
    path(r'^view/(?P<variant_id>\d+)/$', views.view, name='variant_view'),
    
]