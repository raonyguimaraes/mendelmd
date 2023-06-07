from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="settings-index"),    
    path("s3-create/", views.create_s3_credential, name="settings-s3-create"),
    path("s3-edit/<int:pk>)/", views.S3CredentialUpdate.as_view(), name="settings-s3-update"),
    path("s3-view/<int:pk>)/", views.S3CredentialDetailView.as_view(), name="settings-s3-detail"),    
    path("s3-delete/<int:pk>)/", views.S3CredentialDelete.as_view(), name="settings-s3-delete"),
]
