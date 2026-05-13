from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="settings-index"),
    path("profile/", views.profile, name="settings-profile"),
    path("mysubscription/", views.mysubscription, name="settings-mysubscription"),
    path("billing/", views.billing, name="settings-billing"),
    path("create-checkout-session/", views.create_checkout_session, name="create-checkout-session"),
    path("subscription-success/", views.subscription_success, name="subscription-success"),
    path("subscription-cancel/", views.subscription_cancel, name="subscription-cancel"),
    path("create-portal-session/", views.create_portal_session, name="create-portal-session"),

    path("s3-create/", views.create_s3_credential, name="settings-s3-create"),
    path("s3-edit/<int:pk>/", views.S3CredentialUpdate.as_view(), name="settings-s3-update"),
    path("s3-view/<int:pk>/", views.S3CredentialDetailView.as_view(), name="settings-s3-detail"),
    path("s3-delete/<int:pk>/", views.S3CredentialDelete.as_view(), name="settings-s3-delete"),
]
