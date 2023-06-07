from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.models import User

from . import views

urlpatterns = [

    path("", views.index, name="sample_index"),
    path("create_group/", views.create_group, name="create_group"),
    path("groups/", views.SampleGroupList.as_view(), name="samplegroup-list"),
    path("groups/delete/<int:pk>)", views.SampleGroupDelete.as_view(), name="samplegroup_delete"),
    path("groups/<int:pk>)/", views.group_detail, name="samplegroup-view"),
    path("groups/edit/<int:pk>)", views.SampleGroupUpdateView.as_view(), name="samplegroup-edit"),
    path("import_vcf/<int:pk>)/", views.sample_import_vcf, name="sample_import_vcf"),
    # path("delete_group/<int:pk>)", SampleGroupDeleteView.as_view(), {}, "group_delete"),
    path("view/<int:pk>)", views.SampleDetailView.as_view(), name="sample_view"),
    path("bulk_action/", views.bulk_action, name="samples-bulk-action"),
    
    # path("search/", views.search, name="sample_search"),
    # path("action/", views.action, name="sample_action"),

    # path("edit/<int:pk>)", views.sample_update, name="sample_edit"),
    # path("create_analysis/<int:pk>)", views.create_analysis, name="sample_create_analysis"),
    # path("delete/<int:pk>)", views.sample_delete, name="sample_delete"),

   #  path("new", views.ServerCreate.as_view(), name="server_new"),
  	# path("edit/<int:pk>)", views.ServerUpdate.as_view(), name="server_edit"),
  	# path("delete/<int:pk>)", views.ServerDelete.as_view(), name="server_delete"),

    # path("upload/", views.upload, name="upload"),

]
