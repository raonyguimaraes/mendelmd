from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='files-index'),
    url(r'^settings/$', views.settings_index, name='files-settings-index'),
    url(r'^settings/s3-create/$', views.create_s3_credential, name='files-settings-s3-create'),
    url(r'^settings/view/(?P<settings_id>[0-9]+)/$', views.view_setting, name='files-settings-view'),
    # url(r'^view/(?P<project_id>[0-9]+)/$', views.view, name='projects-view'),
]
