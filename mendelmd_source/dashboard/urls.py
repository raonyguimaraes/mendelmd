from django.conf.urls import *

from . import views
urlpatterns = [
    url(r'^$', views.index, name='dashboard'),
    url(r'^bulk_action$', views.bulk_action, name='bulk_action'),   
]