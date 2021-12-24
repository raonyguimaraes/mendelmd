from django.urls import include, path

from . import views

urlpatterns = [
    path(r'', views.index, name='files-index'),
    path(r'import_files/', views.import_files, name='files-import'),
    path(r'upload/', views.upload, name='upload'),
    path(r'view/(?P<file_id>[0-9]+)/', views.view, name='file-view'),
    path(r'update/(?P<pk>[0-9]+)/', views.FileUpdate.as_view(), name='file-update'),
    path(r'delete/(?P<pk>[0-9]+)/', views.FileDelete.as_view(), name='file-delete'),
    path(r'run_task/(?P<pk>[0-9]+)/', views.run_task, name='files-runtask'),
    path(r'bulk_action/', views.bulk_action, name='files-bulk-action'),
    path(r'run_task/', views.run_task, name='files-runtask'),
]
