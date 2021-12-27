from . import views

from django.urls import include, path, re_path

urlpatterns = [
    path('', views.index, name='projects-index'),
    path('create/', views.create, name='projects-create'),
    path('<int:project_id>/', views.view, name='projects-view'),
    path('<int:project_id>/files/', views.project_files, name='project-files'),
    path('update/<int:pk>/', views.ProjectUpdate.as_view(), name='projects-update'),
    path('delete/<int:pk>/', views.ProjectDelete.as_view(), name='projects-delete'),
    path('import_files/<int:project_id>/', views.import_files, name='projects-import-files'),
    path('import_project_files/<int:project_id>/', views.import_project_files, name='import_project_files'),
    path('project_bulk_action/<int:project_id>/', views.bulk_action, name='projects-bulk-action'),
]
