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

                  # url(r'($', views.new_index, name='new_index'),
                  # Examples:
                  # url('($', 'mendelmd.views.home', name='home'),
                  # url('(blog/', include('blog.urls')),
                  path('', views.new_index, name='new_index'),
                  # url('($', views.new_index, name='new_index'),

                  path('docs/', views.docs, name="docs"),

                  path('admin/', admin.site.urls),

                  path('upload/', files.views.upload, name='upload'),

                  path('accounts/', include('allauth.urls')),
                  path('dashboard/', include('dashboard.urls')),
                  path('individuals/', include('individuals.urls')),
                  path('diseases/', include('diseases.urls')),
                  path('genes/', include('genes.urls')),
                  path('variants/', include('variants.urls')),
                  path('cases/', include('cases.urls')),
                  path('filter_analysis/', include('filter_analysis.urls')),
                  # path('(pathway_analysis/', include('apps.pathway_analysis.urls')),
                  path('statistics/', include('stats.urls')),
                  path('databases/', include('databases.urls')),
                  path('projects/', include('projects.urls')),
                  path('select2/', include('django_select2.urls')),
                  path('files/', include('files.urls')),
                  path('samples/', include('samples.urls')),
                  path('settings/', include('settings.urls')),
                  path('tasks/', include('tasks.urls')),
                  path('workers/', include('workers.urls')),
                  path('analyses/', include('analyses.urls')),
                  path('apps/', include('mapps.urls')),
                  path('ecommerce/', include('ecommerce_app.urls')),
                  path('paypal/', include('paypal.standard.ipn.urls')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url('(__debug__/', include(debug_toolbar.urls)),
#     )
