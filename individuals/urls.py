from django.urls import include, path

from individuals.views import IndividualDeleteView, GroupDeleteView
from django.contrib.admin.views.decorators import staff_member_required

from . import views

urlpatterns = [
    path("create/", views.create, name="individual_create"),
    path("edit/<int:individual_id>/", views.edit, name="individual_edit"),
    path("view/<int:individual_id>/", views.view, name="individual_view"),
    path("browse/<int:individual_id>/", views.browse, name="individual_browse"),
    path("delete/<pk>", staff_member_required(IndividualDeleteView.as_view()), {}, "individual_delete"),
    path("annotate/<int:individual_id>/", views.annotate, name="individual_annotate"),
    path("populate/<int:individual_id>/", views.populate, name="individual_populate"),
	path("populate_mongo/<int:individual_id>/", views.populate_mongo, name="individual_populate_mongo"),
    path("", views.list, name="individuals_list"),
	path("download/<int:individual_id>/", views.download, name="individual_download"),
    path("download_annotated/<int:individual_id>/", views.download_annotated, name="individual_download_annotated"),
    path("create_group/", views.create_group, name="create_group"),
    path("view_group/<int:group_id>/", views.view_group, name="view_group"),
    path("delete_group/<int:pk>", GroupDeleteView.as_view(), {}, "group_delete"),
    path("comparison/", views.comparison, name="comparison"),
    
]