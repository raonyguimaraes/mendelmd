from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="webapps_index"),   
    path("import", views.import_apps, name="import_apps"),
    # path("create/", views.create_view, name="app_create"),
    # path('<id>/delete/', views.delete_view, name="app_delete"),
    path('<id>', views.detail_view, name='app_view'),
    path('<id>/move_app/', views.move_app, name="app_move"),
    # path('<id>/update/', views.update_view, name='app_update'),
]
