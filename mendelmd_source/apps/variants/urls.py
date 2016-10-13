
from django.conf.urls import *

from individuals.models import *

from . import views


urlpatterns = [

    url(r'^view/(?P<variant_id>\d+)/$', views.view, name='variant_view'),
    
]