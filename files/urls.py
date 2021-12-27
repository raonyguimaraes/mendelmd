from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='files-index'),
    path('import_files/', views.import_files, name='files-import'),
    path('upload/', views.upload, name='upload'),
    path('view/<int:file_id>/', views.view, name='file-view'),
    path('update/<int:pk>/', views.FileUpdate.as_view(), name='file-update'),
    path('delete/<int:pk>/', views.FileDelete.as_view(), name='file-delete'),
    path('run_task/<int:pk>/', views.run_task, name='files-runtask'),
    path('bulk_action/', views.bulk_action, name='files-bulk-action'),
    path('run_task/', views.run_task, name='files-runtask'),
]
