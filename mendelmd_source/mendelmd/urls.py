from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mendelmd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'mendelmd.views.index', name='index'),
	
	url(r'^docs/$', TemplateView.as_view(template_name='pages/docs.html'), name="docs"),


    url(r'^admin/', include(admin.site.urls)),
	
	url(r'^accounts/', include('allauth.urls')),
    
	url(r'^dashboard/', include('apps.dashboard.urls')),
	url(r'^individuals/', include('apps.individuals.urls')),
    url(r'^diseases/', include('apps.diseases.urls')),
    url(r'^genes/', include('apps.genes.urls')),
    url(r'^variants/', include('apps.variants.urls')),
    url(r'^cases/', include('apps.cases.urls')),
    url(r'^filter_analysis/', include('apps.filter_analysis.urls')),
    # url(r'^pathway_analysis/', include('apps.pathway_analysis.urls')),
    url(r'^statistics/', include('apps.statistics.urls')),
    url(r'^databases/', include('apps.databases.urls')),


    url(r'^select2/', include('django_select2.urls')),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )
