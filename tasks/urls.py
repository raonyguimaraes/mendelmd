from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='tasks-index'),
    path('delete/<int:pk>/', views.TaskDelete.as_view(), name='tasks-delete'),
    # path(r'create/', views.create, name='projects-create'),
    path('view/<int:pk>/', views.TaskDetail.as_view(), name='tasks-view'),
    path('run/<int:task_id>/', views.run_task, name='tasks-run'),
    # path(r'update/<int:pk>/', views.ProjectUpdate.as_view(), name='projects-update'),
    
    # path(r'import_files/(?P<project_id>[0-9]+)/', views.import_files, name='projects-import-files'),
    # path(r'import_project_files/(?P<project_id>[0-9]+)/', views.import_project_files, name='import_project_files'),
    path('bulk_action/', views.bulk_action, name='tasks-bulk-action'),
]
