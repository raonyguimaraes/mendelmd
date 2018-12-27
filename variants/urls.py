from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.index, name='variant_index'),
    url(r'^view/(?P<variant_id>\d+)/$', views.view, name='variant_view'),
    
]