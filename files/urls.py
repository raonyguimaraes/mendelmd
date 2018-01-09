from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='files-index'),
    url(r'^settings/$', views.settings_index, name='files-settings-index'),
    url(r'^settings/view/(?P<settings_id>[0-9]+)/$', views.settings_view, name='files-settings-view'),
    url(r'^import_files/', views.import_files, name='files-import'),
    url(r'^view/(?P<file_id>[0-9]+)/$', views.view, name='file-view'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.FileUpdate.as_view(), name='file-update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.FileDelete.as_view(), name='file-delete'),
    url(r'^bulk_action/$', views.bulk_action, name='files-bulk-action'),
]
