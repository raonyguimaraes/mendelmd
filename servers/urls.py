from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="servers_index"),
    path("import_from_hetzner", views.import_from_hetzner, name="import_from_hetzner"),
    path("add_sshkey_to_servers", views.add_sshkey_to_servers, name="add_sshkey_to_servers"),
    path("update_usage", views.update_usage, name="update_usage"),
    
]
