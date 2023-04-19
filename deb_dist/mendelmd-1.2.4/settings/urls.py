from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='settings-index'),    
    url(r'^s3-create/$', views.create_s3_credential, name='settings-s3-create'),
    url(r'^s3-edit/(?P<pk>[0-9]+)/$', views.S3CredentialUpdate.as_view(), name='settings-s3-update'),
    url(r'^s3-view/(?P<pk>[0-9]+)/$', views.S3CredentialDetailView.as_view(), name='settings-s3-detail'),    
    url(r'^s3-delete/(?P<pk>[0-9]+)/$', views.S3CredentialDelete.as_view(), name='settings-s3-delete'),
]
