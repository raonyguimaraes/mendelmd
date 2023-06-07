# -*- coding: utf-8 -*-
"""
Django-Select2 URL configuration.

Add `django_select` to your ``urlconf`` **if** you use any 'Model' fields::

    url(r'^select2/', include('django_select2.urls')),

"""
from __future__ import absolute_import, unicode_literals

from django.urls import include, path

from .views import AutoResponseView

urlpatterns = [
    path("fields/auto.json",
        AutoResponseView.as_view(), name="django_select2-json"),
]
