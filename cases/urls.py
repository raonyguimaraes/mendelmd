from django.urls import include, path
from django.views.generic import TemplateView

from cases.views import CaseDeleteView

from . import views


urlpatterns = [

    path("", views.cases_list, name='cases_list'),
    path("create/", views.create_case, name='create_case'),
    path("delete/<int:pk>", CaseDeleteView.as_view(), {}, 'delete_case'),
    path("edit/<int:case_id>/", views.edit, name='edit_case'),
    path("view/<int:case_id>/", views.view_case, name='view_case'),
    path("view/<int:case_id>/", views.view_case, name='view_case'),
    path("analyze/<int:case_id>/<slug:analysis>/<slug:inheritance>/", views.analysis, name='analyze_case'),
    

    # path("^new/", IndividualCreateView.as_view(), {}, 'individual-new'),
    # path("^delete/(?P<pk>\d+)", IndividualDeleteView.as_view(), {}, 'individual-delete'),
    # path("^edit/(?P<individual_id>\d+)/", 'edit', name='individual_edit'),
    
    # path("^success/", TemplateView.as_view(template_name='individuals/sucess.html'), name="sucess"),

    # path("^view/(?P<individual_id>\d+)/", 'view', name='individual_view'),
    
    # path("^view/(?P<individual_id>\d+)/medical_conditions/", 'view_medical_conditions', name='individual_view_medical_conditions'),
    # path("^view/(?P<individual_id>\d+)/medicines/", 'view_medicines', name='individual_view_medicines'),
    # path("^view/(?P<individual_id>\d+)/hgmd/", 'view_hgmd_mutations', name='view_hgmd_mutations'),
    


    # path("^browse/(?P<individual_id>\d+)/", 'browse', name='individual_browse'),
    # path("^export_csv/(?P<individual_id>\d+)/", 'export_csv', name='export_csv'),
    # path("^populate/(?P<individual_id>\d+)/", 'populate', name='individual_populate'),
    # path("^populate_mongo/(?P<individual_id>\d+)/", 'populate_mongo', name='individual_populate_mongo'),
    
    # path("^annotate/(?P<individual_id>\d+)/", 'annotate', name='individual_annotate'),
    # path("^download/(?P<individual_id>\d+)/", 'download', name='individual_download'),
    # path("^download_annotated/(?P<individual_id>\d+)/", 'download_annotated', name='individual_download_annotated'),
    # path("^download_annovar/(?P<individual_id>\d+)/", 'download_annova", name='individual_download_annova"),
    # path("^download_csv/(?P<individual_id>\d+)/", 'download_csv', name='individual_download_csv'),
    # path("^find_individual_diseases/(?P<individual_id>\d+)/", 'find_individual_diseases', name='find_individual_diseases'),
    # path("^find_individual_medicines/(?P<individual_id>\d+)/", 'find_individual_medicines', name='find_individual_medicines'),
    # path("^create_group/", 'create_group', name='create_group'),
    # path("^delete_group/(?P<pk>\d+)", GroupDeleteView.as_view(), {}, 'group_delete'),
    # #path("^delete_group/(?P<group_id>\d+)/", 'delete_group', name='delete_group'),
    # path("^comparison/", 'comparison', name='comparison'),
    # path("^export_comparison/", 'export_comparison', name='export_comparison'),   
]