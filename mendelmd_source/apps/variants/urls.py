
from django.conf.urls import patterns, url

from individuals.models import *
from variants.views import *

urlpatterns = patterns('variants.views',

    url(r'^view/(?P<variant_id>\d+)/$', 'view', name='variant_view'),
    
)