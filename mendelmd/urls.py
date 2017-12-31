from django.conf.urls import *

from django.contrib import admin

from django.views.generic import TemplateView

admin.autodiscover()

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'mendelmd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),

	url(r'^docs/$', views.docs, name="docs"),


    url(r'^admin/', admin.site.urls),


	url(r'^accounts/', include('allauth.urls')),

	url(r'^dashboard/', include('dashboard.urls')),
	url(r'^individuals/', include('individuals.urls')),
    url(r'^diseases/', include('diseases.urls')),
    url(r'^genes/', include('genes.urls')),
    url(r'^variants/', include('variants.urls')),
    url(r'^cases/', include('cases.urls')),
    url(r'^filter_analysis/', include('filter_analysis.urls')),
    # url(r'^pathway_analysis/', include('apps.pathway_analysis.urls')),
    # url(r'^statistics/', include('statistics.urls')),
    url(r'^databases/', include('databases.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^files/', include('files.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )
