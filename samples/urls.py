from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.models import User

from . import views

urlpatterns = [

    url(r'^$', views.index, name='sample_index'),

    # url(r'^view/(?P<pk>\d+)$', views.view, name='sample_view'),
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