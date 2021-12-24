from django.contrib import admin

from django.views.generic import TemplateView

admin.autodiscover()

from django.conf import settings

from django.conf.urls.static import static

from . import views

import files.views

from django.urls import path


urlpatterns = [
    # Examples:
    # url(r'^$', 'mendelmd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    path(r'^$', views.new_index, name='new_index'),
                  # url(r'^$', views.new_index, name='new_index'),

                  path(r'^docs/$', views.docs, name="docs"),

    path('admin/', admin.site.urls),

    path(r'^upload/', files.views.upload, name='upload'),

    path(r'^accounts/', include('allauth.paths')),
    path(r'^dashboard/', include('dashboard.paths')),
    path(r'^individuals/', include('individuals.paths')),
    path(r'^diseases/', include('diseases.paths')),
    path(r'^genes/', include('genes.paths')),
    path(r'^variants/', include('variants.paths')),
    path(r'^cases/', include('cases.paths')),
    path(r'^filter_analysis/', include('filter_analysis.paths')),
    # path(r'^pathway_analysis/', include('apps.pathway_analysis.paths')),
    path(r'^statistics/', include('stats.paths')),
    path(r'^databases/', include('databases.paths')),
    path(r'^projects/', include('projects.paths')),
    path(r'^select2/', include('django_select2.paths')),
    path(r'^files/', include('files.paths')),
    path(r'^samples/', include('samples.paths')),
    path(r'^settings/', include('settings.paths')),
    path(r'^tasks/', include('tasks.paths')),
    path(r'^workers/', include('workers.paths')),
    path(r'^analyses/', include('analyses.paths')),
    path(r'^apps/', include('mapps.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )
