from django.conf.urls import *
from django.views.generic import TemplateView

from cases.views import CaseDeleteView

from . import views


urlpatterns = [

    url(r'^$', views.cases_list, name='cases_list'),
    url(r'^create/$', views.create_case, name='create_case'),
    url(r'^delete/(?P<pk>\d+)$', CaseDeleteView.as_view(), {}, 'delete_case'),
    url(r'^edit/(?P<case_id>\d+)/$', views.edit, name='edit_case'),
    url(r'^view/(?P<case_id>\d+)/$', views.view_case, name='view_case'),
    url(r'^view/(?P<case_id>\d+)/$', views.view_case, name='view_case'),
    url(r'^analyze/(?P<case_id>\d+)/(?P<analysis>\w+)/(?P<inheritance>\w+)/$', views.analysis, name='analyze_case'),
    

    # url(r'^new/$', IndividualCreateView.as_view(), {}, 'individual-new'),
    # url(r'^delete/(?P<pk>\d+)$', IndividualDeleteView.as_view(), {}, 'individual-delete'),
    # url(r'^edit/(?P<individual_id>\d+)/$', 'edit', name='individual_edit'),
    
    # url(r'^success/$', TemplateView.as_view(template_name='individuals/sucess.html'), name="sucess"),

    # url(r'^view/(?P<individual_id>\d+)/$', 'view', name='individual_view'),
    
    # url(r'^view/(?P<individual_id>\d+)/medical_conditions/$', 'view_medical_conditions', name='individual_view_medical_conditions'),
    # url(r'^view/(?P<individual_id>\d+)/medicines/$', 'view_medicines', name='individual_view_medicines'),
    # url(r'^view/(?P<individual_id>\d+)/hgmd/$', 'view_hgmd_mutations', name='view_hgmd_mutations'),
    


    # url(r'^browse/(?P<individual_id>\d+)/$', 'browse', name='individual_browse'),
    # url(r'^export_csv/(?P<individual_id>\d+)/$', 'export_csv', name='export_csv'),
    # url(r'^populate/(?P<individual_id>\d+)/$', 'populate', name='individual_populate'),
    # url(r'^populate_mongo/(?P<individual_id>\d+)/$', 'populate_mongo', name='individual_populate_mongo'),
    
    # url(r'^annotate/(?P<individual_id>\d+)/$', 'annotate', name='individual_annotate'),
    # url(r'^download/(?P<individual_id>\d+)/$', 'download', name='individual_download'),
    # url(r'^download_annotated/(?P<individual_id>\d+)/$', 'download_annotated', name='individual_download_annotated'),
    # url(r'^download_annovar/(?P<individual_id>\d+)/$', 'download_annovar', name='individual_download_annovar'),
    # url(r'^download_csv/(?P<individual_id>\d+)/$', 'download_csv', name='individual_download_csv'),
    # url(r'^find_individual_diseases/(?P<individual_id>\d+)/$', 'find_individual_diseases', name='find_individual_diseases'),
    # url(r'^find_individual_medicines/(?P<individual_id>\d+)/$', 'find_individual_medicines', name='find_individual_medicines'),
    # url(r'^create_group/$', 'create_group', name='create_group'),
    # url(r'^delete_group/(?P<pk>\d+)$', GroupDeleteView.as_view(), {}, 'group_delete'),
    # #url(r'^delete_group/(?P<group_id>\d+)/$', 'delete_group', name='delete_group'),
    # url(r'^comparison/$', 'comparison', name='comparison'),
    # url(r'^export_comparison/$', 'export_comparison', name='export_comparison'),   
]