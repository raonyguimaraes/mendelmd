from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="servers_index"),
    path("import_from_hetzner", views.import_from_hetzner, name="import_from_hetzner"),
    path("add_sshkey_to_servers", views.add_sshkey_to_servers, name="add_sshkey_to_servers"),
    path("update_usage", views.update_usage, name="update_usage"),
    path("reboot", views.reboot, name="servers_reboot"),
    path("check_status", views.check_status, name="servers_check_status"),


    path("create/", views.create, name="server_create"),
    path('<id>/delete/', views.delete_view, name="server_delete"),
    path('<id>/terminate/', views.terminate_view, name="server_terminate"),
    path('<id>', views.detail_view, name='server_view'),
    path('<id>/update/', views.update_view, name='server_update'),
    path("servers_bulk_action/", views.servers_bulk_action, name="servers_bulk_action"), 
    # path("edit/<int:individual_id>/", views.edit, name="individual_edit"),
    # path("view/<int:individual_id>/", views.view, name="individual_view"),

]
