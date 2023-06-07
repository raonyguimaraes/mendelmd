from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="tasks-index"),
    path("delete/<int:pk>/", views.TaskDelete.as_view(), name="tasks-delete"),
    # path("create/", views.create, name="projects-create"),
    path("view/<int:pk>/", views.TaskDetail.as_view(), name="tasks-view"),
    path("run/<int:task_id>/", views.run_task, name="tasks-run"),
    # path("update/<pk>)/", views.ProjectUpdate.as_view(), name="projects-update"),
    
    # path("import_files/<project_id>)/", views.import_files, name="projects-import-files"),
    # path("import_project_files/<project_id>)/", views.import_project_files, name="import_project_files"),
    path("bulk_action/", views.bulk_action, name="tasks-bulk-action"),
]
