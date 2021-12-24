from . import views
from django.urls import include, path


urlpatterns = [
    path(r'', views.index, name='worker-list'),
    path(r'launch_worker/', views.launch, name='worker-launch'),
    path(r'update/(?P<pk>[0-9]+)/', views.update, name='worker-update'),
    path(r'install/(?P<pk>[0-9]+)/', views.install, name='worker-install'),
    path(r'terminate/(?P<pk>[0-9]+)/', views.terminate, name='worker-terminate'),
    path(r'delete/(?P<pk>\d+)/', views.WorkerDelete.as_view(), name='worker-delete'),
    path(r'action/', views.action, name='worker-bulk-action'),
]
