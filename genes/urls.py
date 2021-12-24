from django.conf import settings
from django.urls import include, path
from .views import ListGene, GeneDetail, GenesetDetailView
from django.contrib import admin
admin.autodiscover()
from genes.models import GeneList

from . import views

from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path(r"populate/", views.populate, name="genes_populate"),#inser genes from hgnc
    path(r"populatego/", views.populate_fromgo, name="populate_fromgo"),#insert data from gene_go_terms
    #path(r"populatetermsgo/", 'genes.views.populate_termsfromgo', name="populate_termsfromgo"),#insert data from go.obo
    #path(r"", 'genes.views.list', name="genes_list"),
    path(r'', login_required(ListGene.as_view()), name="genes_list"),
    path(r'populate_cgd/', views.populate_cgd, name='populate_cgd'),
    path(r'create_cgd_categories/', views.create_cgd_categories, name='create_cgd_categories'),
    path(r'geneontology/', views.geneontology, name="geneontology"),
    # path(r'geneontology/(?P<go_id>(?!creategroup|signup|signin)[\%\:\~\.\-\w]+)/', views.geneontology_view, name="geneontology_view"),
    path(r'(?P<pk>\d+)/', login_required(GeneDetail.as_view()), name='gene_detail'),
    # path(r'(?P<gene_name>(?!creategroup|signup|signin)[\"\@\:\~\.\-\w]+)/', views.view, name='gene_view'),
    path(r'creategroup/', views.creategroup, name='gene_group_create'),
    path(r'geneset/add/', views.genesetcreate, name='geneset-create'),
    path(r'geneset/view/(?P<pk>[\w\d]+)', login_required(GenesetDetailView.as_view()), name='geneset-detail'),
    path(r'geneset/delete/(?P<pk>[\w\d]+)', views.delete_genelist, name='geneset-delete'),
    ]