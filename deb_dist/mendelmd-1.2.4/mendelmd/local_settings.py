#!/usr/bin/env python
# -*- coding: utf-8 -*-
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mendelmd',
    }
}

SECRET_KEY = '*efl#$$!@93)8397wwf8hy3873&ad8h7d2w-JKFCGYURaonyGUimaraesCorreayus5mzcx&@'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mendelmd1@gmail.com'
EMAIL_HOST_PASSWORD = '3mp1r1cL0g1c'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEBUG=True
#STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, "static"),
#    '/var/www/html/static/',
#)i

