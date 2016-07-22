from django.conf.urls import patterns, include, url

urlpatterns = patterns('dashboard.views',
    url(r'^$', 'index', name='dashboard'),
    url(r'^bulk_action$', 'bulk_action', name='bulk_action'),

    
)