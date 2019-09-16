from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.models import User

from . import views

urlpatterns = [

    url(r'^$', views.index, name='sample_index'),
    url(r'^create_group/$', views.create_group, name='create_group'),
    url(r'^groups/$', views.SampleGroupList.as_view(), name='samplegroup-list'),
    url(r'^groups/delete/(?P<pk>\d+)$', views.SampleGroupDelete.as_view(), name='samplegroup_delete'),
    url(r'^groups/(?P<pk>\d+)/$', views.group_detail, name='samplegroup-view'),
    url(r'^groups/edit/(?P<pk>\d+)$', views.SampleGroupUpdateView.as_view(), name='samplegroup-edit'),
    url(r'^import_vcf/(?P<pk>\d+)/$', views.sample_import_vcf, name='sample_import_vcf'),
    # url(r'^delete_group/(?P<pk>\d+)$', SampleGroupDeleteView.as_view(), {}, 'group_delete'),
    url(r'^view/(?P<pk>\d+)$', views.SampleDetailView.as_view(), name='sample_view'),
    url(r'^bulk_action/$', views.bulk_action, name='samples-bulk-action'),
    
    # url(r'^search/$', views.search, name='sample_search'),
    # url(r'^action/$', views.action, name='sample_action'),

    # url(r'^edit/(?P<pk>\d+)$', views.sample_update, name='sample_edit'),
    # url(r'^create_analysis/(?P<pk>\d+)$', views.create_analysis, name='sample_create_analysis'),
    # url(r'^delete/(?P<pk>\d+)$', views.sample_delete, name='sample_delete'),

   #  url(r'^new$', views.ServerCreate.as_view(), name='server_new'),
  	# url(r'^edit/(?P<pk>\d+)$', views.ServerUpdate.as_view(), name='server_edit'),
  	# url(r'^delete/(?P<pk>\d+)$', views.ServerDelete.as_view(), name='server_delete'),

    # url(r'^upload/', views.upload, name='upload'),

]
