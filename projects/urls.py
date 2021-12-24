from . import views

from django.urls import include, path


urlpatterns = [
    path(r'', views.index, name='projects-index'),
    path(r'create/', views.create, name='projects-create'),
    path(r'(?P<project_id>[0-9]+)/', views.view, name='projects-view'),
    path(r'(?P<project_id>[0-9]+)/files/', views.project_files, name='project-files'),
    path(r'update/(?P<pk>[0-9]+)/', views.ProjectUpdate.as_view(), name='projects-update'),
    path(r'delete/(?P<pk>[0-9]+)/', views.ProjectDelete.as_view(), name='projects-delete'),
    path(r'import_files/(?P<project_id>[0-9]+)/', views.import_files, name='projects-import-files'),
    path(r'import_project_files/(?P<project_id>[0-9]+)/', views.import_project_files, name='import_project_files'),
    path(r'project_bulk_action/(?P<project_id>[0-9]+)/', views.bulk_action, name='projects-bulk-action'),
]
