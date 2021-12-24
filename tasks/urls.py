
from . import views

from django.urls import include, path


urlpatterns = [
    path(r'', views.index, name='tasks-index'),
    path(r'delete/(?P<pk>[0-9]+)/', views.TaskDelete.as_view(), name='tasks-delete'),
    # path(r'create/', views.create, name='projects-create'),
    path(r'view/(?P<pk>[0-9]+)/', views.TaskDetail.as_view(), name='tasks-view'),
    path(r'run/(?P<task_id>[0-9]+)/', views.run_task, name='tasks-run'),
    # path(r'update/(?P<pk>[0-9]+)/', views.ProjectUpdate.as_view(), name='projects-update'),
    
    # path(r'import_files/(?P<project_id>[0-9]+)/', views.import_files, name='projects-import-files'),
    # path(r'import_project_files/(?P<project_id>[0-9]+)/', views.import_project_files, name='import_project_files'),
    path(r'bulk_action/', views.bulk_action, name='tasks-bulk-action'),
]
