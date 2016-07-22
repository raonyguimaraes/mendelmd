from django.conf import settings
from django.conf.urls import *
from .views import ListGene, GeneDetail, GenesetDetailView
from django.contrib import admin
admin.autodiscover()
from genes.models import GeneList

urlpatterns = patterns("",
    url(r"^populate/$", 'genes.views.populate', name="genes_populate"),#inser genes from hgnc
    url(r"^populatego/$", 'genes.views.populate_fromgo', name="populate_fromgo"),#insert data from gene_go_terms
    #url(r"^populatetermsgo/$", 'genes.views.populate_termsfromgo', name="populate_termsfromgo"),#insert data from go.obo
    #url(r"^$", 'genes.views.list', name="genes_list"),
    url(r'^$', ListGene.as_view(), name="genes_list"),

    url(r'^populate_cgd/$', 'genes.views.populate_cgd', name='populate_cgd'),
    url(r'^create_cgd_categories/$', 'genes.views.create_cgd_categories', name='create_cgd_categories'),
    
    
    url(r'^geneontology/$', 'genes.views.geneontology', name="geneontology"),
    url(r'^geneontology/(?P<go_id>(?!creategroup|signup|signin)[\%\:\~\.\-\w]+)/$', 'genes.views.geneontology_view', name="geneontology_view"),
    
    url(r'^(?P<pk>\d+)/$', GeneDetail.as_view(), name='gene_detail'),
    
    
    url(r'^(?P<gene_name>(?!creategroup|signup|signin)[\"\@\:\~\.\-\w]+)/$', 'genes.views.view', name='gene_view'),
    url(r'^creategroup/$', 'genes.views.creategroup', name='gene_group_create'),

    url(r'^geneset/add/$', 'genes.views.genesetcreate', name='geneset-create'),
    url(r'^geneset/view/(?P<pk>[\w\d]+)$', GenesetDetailView.as_view(), name='geneset-detail'),
    url(r'^geneset/delete/(?P<pk>[\w\d]+)$', 'genes.views.delete_genelist', name='geneset-delete'),

    

    )