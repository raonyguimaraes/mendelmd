from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='projects-index'),
    url(r'^create/$', views.create, name='projects-create'),
    url(r'^view/(?P<project_id>[0-9]+)/$', views.view, name='projects-view'),
    url(r'^import_files/(?P<project_id>[0-9]+)/$', views.import_files, name='projects-import-files'),
    # url(r'^articles/([0-9]{4})/$', views.year_archive),
    # url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    # url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]
