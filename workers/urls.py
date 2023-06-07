from django.urls import include, path


from . import views

urlpatterns = [
    path("", views.index, name="worker-list"),
    path("launch_worker/", views.launch, name="worker-launch"),
    path("update/(<int:pk>/", views.update, name="worker-update"),
    path("install/<int:pk>/", views.install, name="worker-install"),
    path("terminate/<int:pk>/", views.terminate, name="worker-terminate"),
    path("delete/<int:pk>/", views.WorkerDelete.as_view(),
        name="worker-delete"),
    path("action/", views.action, name="worker-bulk-action"),
]