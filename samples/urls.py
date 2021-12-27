from django.contrib import admin
from django.contrib.auth.models import User

from . import views
from django.urls import include, path


urlpatterns = [

    path(r'', views.index, name='sample_index'),
    path(r'create_group/', views.create_group, name='create_group'),
    path(r'groups/', views.SampleGroupList.as_view(), name='samplegroup-list'),
    path(r'groups/delete/(?P<pk>\d+)', views.SampleGroupDelete.as_view(), name='samplegroup_delete'),
    path(r'groups/(?P<pk>\d+)/', views.group_detail, name='samplegroup-view'),
    path(r'groups/edit/(?P<pk>\d+)', views.SampleGroupUpdateView.as_view(), name='samplegroup-edit'),
    path(r'import_vcf/(?P<pk>\d+)/', views.sample_import_vcf, name='sample_import_vcf'),
    # path(r'delete_group/(?P<pk>\d+)', SampleGroupDeleteView.as_view(), {}, 'group_delete'),
    path(r'view/(?P<pk>\d+)', views.SampleDetailView.as_view(), name='sample_view'),
    path(r'bulk_action/', views.bulk_action, name='samples-bulk-action'),
    
    # path(r'search/', views.search, name='sample_search'),
    # path(r'action/', views.action, name='sample_action'),

    # path(r'edit/(?P<pk>\d+)', views.sample_update, name='sample_edit'),
    # path(r'create_analysis/(?P<pk>\d+)', views.create_analysis, name='sample_create_analysis'),
    # path(r'delete/(?P<pk>\d+)', views.sample_delete, name='sample_delete'),

   #  path(r'new', views.ServerCreate.as_view(), name='server_new'),
  	# path(r'edit/(?P<pk>\d+)', views.ServerUpdate.as_view(), name='server_edit'),
  	# path(r'delete/(?P<pk>\d+)', views.ServerDelete.as_view(), name='server_delete'),

    # path(r'upload/', views.upload, name='upload'),

]
