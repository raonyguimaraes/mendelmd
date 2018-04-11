from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.index, name='apps-index'),
    url(r'^create/$', views.AppCreate.as_view(), name='apps-create'),
    url(r'update/(?P<pk>\d+)/$', views.AppUpdate.as_view(), name='apps-update'),
    
]