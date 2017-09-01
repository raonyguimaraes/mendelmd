from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.index),
    # url(r'^terminate/(?P<pk>[0-9]+)/$', views.terminate, name='worker-terminate'),
    # url(r'^delete/(?P<pk>\d+)/$', views.WorkerDelete.as_view(),
    #     name='worker_delete'),
]