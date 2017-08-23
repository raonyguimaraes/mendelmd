from django.conf import settings
from django.conf.urls import *
from .views import ListGene, GeneDetail, GenesetDetailView
from django.contrib import admin
admin.autodiscover()
from genes.models import GeneList

from . import views

from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r"^populate/$", views.populate, name="genes_populate"),#inser genes from hgnc
    url(r"^populatego/$", views.populate_fromgo, name="populate_fromgo"),#insert data from gene_go_terms
    #url(r"^populatetermsgo/$", 'genes.views.populate_termsfromgo', name="populate_termsfromgo"),#insert data from go.obo
    #url(r"^$", 'genes.views.list', name="genes_list"),
    url(r'^$', login_required(ListGene.as_view()), name="genes_list"),
    url(r'^populate_cgd/$', views.populate_cgd, name='populate_cgd'),
    url(r'^create_cgd_categories/$', views.create_cgd_categories, name='create_cgd_categories'),
    url(r'^geneontology/$', views.geneontology, name="geneontology"),
    url(r'^geneontology/(?P<go_id>(?!creategroup|signup|signin)[\%\:\~\.\-\w]+)/$', views.geneontology_view, name="geneontology_view"),
    url(r'^(?P<pk>\d+)/$', login_required(GeneDetail.as_view()), name='gene_detail'),
    url(r'^(?P<gene_name>(?!creategroup|signup|signin)[\"\@\:\~\.\-\w]+)/$', views.view, name='gene_view'),
    url(r'^creategroup/$', views.creategroup, name='gene_group_create'),
    url(r'^geneset/add/$', views.genesetcreate, name='geneset-create'),
    url(r'^geneset/view/(?P<pk>[\w\d]+)$', login_required(GenesetDetailView.as_view()), name='geneset-detail'),
    url(r'^geneset/delete/(?P<pk>[\w\d]+)$', views.delete_genelist, name='geneset-delete'),
    ]