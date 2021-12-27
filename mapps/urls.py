from django.conf.urls import *

from . import views

from django.urls import path


urlpatterns = [
    path(r'', views.index, name='apps-index'),
    path(r'create/$', views.AppCreate.as_view(), name='apps-create'),
    path(r'update/(?P<pk>\d+)/$', views.AppUpdate.as_view(), name='apps-update'),
    
]