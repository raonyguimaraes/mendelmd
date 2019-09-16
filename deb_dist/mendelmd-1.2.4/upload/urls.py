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
    url(r'^$', views.upload, name='upload'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

