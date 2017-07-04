from django.conf.urls import *

from individuals.views import IndividualDeleteView, GroupDeleteView
from django.contrib.admin.views.decorators import staff_member_required

from . import views

urlpatterns = [
    url(r'^create/$', views.create, name='individual_create'),
    url(r'^edit/(?P<individual_id>[0-9]+)/$', views.edit, name='individual_edit'),
    url(r'^view/(?P<individual_id>\d+)/$', views.view, name='individual_view'),
    url(r'^browse/(?P<individual_id>\d+)/$', views.browse, name='individual_browse'),
    url(r'^delete/(?P<pk>\d+)$', staff_member_required(IndividualDeleteView.as_view()), {}, 'individual_delete'),
    url(r'^annotate/(?P<individual_id>\d+)/$', views.annotate, name='individual_annotate'),
    url(r'^populate/(?P<individual_id>\d+)/$', views.populate, name='individual_populate'),
	url(r'^populate_mongo/(?P<individual_id>\d+)/$', views.populate_mongo, name='individual_populate_mongo'),
    url(r'^$', views.list, name='individuals_list'),
	url(r'^download/(?P<individual_id>\d+)/$', views.download, name='individual_download'),
    url(r'^download_annotated/(?P<individual_id>\d+)/$', views.download_annotated, name='individual_download_annotated'),
    url(r'^create_group/$', views.create_group, name='create_group'),
    url(r'^view_group/(?P<group_id>\d+)/$', views.view_group, name='view_group'),
    url(r'^delete_group/(?P<pk>\d+)$', GroupDeleteView.as_view(), {}, 'group_delete'),
    url(r'^comparison/$', views.comparison, name='comparison'),
    
]