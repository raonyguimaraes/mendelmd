from django.contrib import admin

from django.views.generic import TemplateView

admin.autodiscover()

from django.conf import settings

from django.conf.urls.static import static
from django.conf.urls import include

from django.urls import path

from . import views

import files.views

from django.urls import path


urlpatterns = [
    # Examples:
    #path(r'', views.index, name='index'),

    path(r'docs/', views.docs, name="docs"),
    path(r'', views.new_index, name='new_index'),
                  # url(r'($', views.new_index, name='new_index'),

    path(r'(docs/', views.docs, name="docs"),

    path('admin/', admin.site.urls),

    path(r'(upload/', files.views.upload, name='upload'),

    path('accounts/', include('allauth.urls')),
    path(r'(dashboard/', include('dashboard.urls')),
    path(r'(individuals/', include('individuals.urls')),
    path(r'(diseases/', include('diseases.urls')),
    path(r'(genes/', include('genes.urls')),
    path(r'(variants/', include('variants.urls')),
    path(r'(cases/', include('cases.urls')),
    path(r'(filter_analysis/', include('filter_analysis.urls')),
    # path(r'(pathway_analysis/', include('apps.pathway_analysis.urls')),
    path(r'(statistics/', include('stats.urls')),
    path(r'(databases/', include('databases.urls')),
    path(r'(projects/', include('projects.urls')),
    path(r'(select2/', include('django_select2.urls')),
    path("select2/", include("django_select2.urls")),
    path(r'(files/', include('files.urls')),
    path(r'(samples/', include('samples.urls')),
    path(r'(settings/', include('settings.urls')),
    path(r'(tasks/', include('tasks.urls')),
    path(r'(workers/', include('workers.urls')),
    path(r'(analyses/', include('analyses.urls')),
    path(r'(apps/', include('mapps.urls')),
    path('ecommerce/', include('ecommerce_app.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'(__debug__/', include(debug_toolbar.urls)),
#     )
