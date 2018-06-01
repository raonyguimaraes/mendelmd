from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.index, name='worker-list'),
    url(r'^launch_worker/$', views.launch, name='worker-launch'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.update, name='worker-update'),
    url(r'^install/(?P<pk>[0-9]+)/$', views.install, name='worker-install'),
    url(r'^terminate/(?P<pk>[0-9]+)/$', views.terminate, name='worker-terminate'),
    url(r'^delete/(?P<pk>\d+)/$', views.WorkerDelete.as_view(),
        name='worker-delete'),
    url(r'^action/$', views.action, name='worker-bulk-action'),
]
