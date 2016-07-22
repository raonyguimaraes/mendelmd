from django.conf.urls import patterns, url

from individuals.views import IndividualDeleteView, GroupDeleteView


urlpatterns = patterns('individuals.views',
    url(r'^create/$', 'create', name='individual_create'),
    url(r'^edit/(?P<individual_id>[0-9]+)/$', 'edit', name='individual_edit'),
    url(r'^view/(?P<individual_id>\d+)/$', 'view', name='individual_view'),
    url(r'^browse/(?P<individual_id>\d+)/$', 'browse', name='individual_browse'),
    url(r'^delete/(?P<pk>\d+)$', IndividualDeleteView.as_view(), {}, 'individual_delete'),
    url(r'^annotate/(?P<individual_id>\d+)/$', 'annotate', name='individual_annotate'),
    url(r'^populate/(?P<individual_id>\d+)/$', 'populate', name='individual_populate'),
	url(r'^populate_mongo/(?P<individual_id>\d+)/$', 'populate_mongo', name='individual_populate_mongo'),
    url(r'^$', 'list', name='individuals_list'),
	url(r'^download/(?P<individual_id>\d+)/$', 'download', name='individual_download'),
    url(r'^download_annotated/(?P<individual_id>\d+)/$', 'download_annotated', name='individual_download_annotated'),

    url(r'^create_group/$', 'create_group', name='create_group'),
    url(r'^view_group/(?P<group_id>\d+)/$', 'view_group', name='view_group'),
    url(r'^delete_group/(?P<pk>\d+)$', GroupDeleteView.as_view(), {}, 'group_delete'),
    url(r'^comparison/$', 'comparison', name='comparison'),
    
)