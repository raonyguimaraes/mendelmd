from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='files-index'),
    url(r'^import_files/', views.import_files, name='files-import'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^view/(?P<file_id>[0-9]+)/$', views.view, name='file-view'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.FileUpdate.as_view(), name='file-update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.FileDelete.as_view(), name='file-delete'),
    url(r'^run_task/(?P<pk>[0-9]+)/$', views.run_task, name='files-runtask'),
    url(r'^bulk_action/$', views.bulk_action, name='files-bulk-action'),
    url(r'^run_task/$', views.run_task, name='files-runtask'),
]
