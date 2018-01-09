from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='tasks-index'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.TaskDelete.as_view(), name='tasks-delete'),
    # url(r'^create/$', views.create, name='projects-create'),
    url(r'^view/(?P<pk>[0-9]+)/$', views.TaskDetail.as_view(), name='tasks-view'),
    url(r'^run/(?P<task_id>[0-9]+)/$', views.run_task, name='tasks-run'),
    # url(r'^update/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='projects-update'),
    
    # url(r'^import_files/(?P<project_id>[0-9]+)/$', views.import_files, name='projects-import-files'),
    # url(r'^import_project_files/(?P<project_id>[0-9]+)/$', views.import_project_files, name='import_project_files'),
    url(r'^bulk_action/$', views.bulk_action, name='tasks-bulk-action'),
]
