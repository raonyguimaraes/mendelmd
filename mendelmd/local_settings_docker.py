#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

SECRET_KEY = os.environ.get('SECRET_KEY', '*efl#$$!@93)8397wwf8hy3873&ad8h7d2w-JKFCGYURaonyGUimaraesCorreayus5mzcx&@')

DEBUG = False

ALLOWED_HOSTS = ['dev.mendelmd.org', 'mendelmd.org', 'www.mendelmd.org', '144.76.63.166', 'localhost', '127.0.0.1']

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Required for AJAX uploads through an nginx reverse proxy.
# Without this, Django's CSRF check compares Origin: https://mendelmd.org
# against the internal Host header (e.g. localhost) and returns 403.
CSRF_TRUSTED_ORIGINS = [
    'https://dev.mendelmd.org',
    'https://mendelmd.org',
    'https://www.mendelmd.org',
]

# Media files (uploaded VCF files, etc.)
MEDIA_ROOT = BASE_DIR   # files land at /code/genomes/<user>/<id>/
MEDIA_URL = '/media/'
