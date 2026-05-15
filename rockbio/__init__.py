from __future__ import absolute_import, unicode_literals

# Compatibility shim — project renamed from rockbio to mendelmd
from mendelmd.celery import app as celery_app

__all__ = ['celery_app']
