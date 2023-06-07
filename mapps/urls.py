from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="apps-index"),
    path("create/", views.AppCreate.as_view(), name="apps-create"),
    path("update/<int:pk>/", views.AppUpdate.as_view(), name="apps-update"),
    
]