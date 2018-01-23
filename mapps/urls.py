from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.index, name='apps-index'),

    
]