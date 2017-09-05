"""
Django settings for mendelmd project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*efl#$$!@93)8397wwf8hy387"&^%3&ad8h7d2w-yus5mzcx&@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    #external libs
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'django_select2',

    # 'djcelery',
    'celery',
    # 'kombu.transport.django',
    # 'djkombu',
    'django_celery_results',
    'django_celery_beat',

    #private apps

    'dashboard',
    'individuals',
    'variants',
    'diseases',
    'genes',
    'pagination',
    'cases',
    'filter_analysis',
    'pathway_analysis',
    'statistics',
    'databases',
    'projects',
    'files',
    'app',
    'tasks',
    'workers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'mendelmd.urls'

WSGI_APPLICATION = 'mendelmd.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'mendelmd.sqlite3'),
    }
}



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = os.path.join(BASE_DIR,'static/')

STATIC_ROOT = '/var/www/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.contrib.auth.context_processors.auth",
#     "django.core.context_processors.debug",
#     "django.core.context_processors.i18n",
#     "django.core.context_processors.media",
#     "django.core.context_processors.static",
#     "django.core.context_processors.tz",
#     "django.contrib.messages.context_processors.messages",
#     "django.core.context_processors.request",
#     # allauth specific context processors
#     "allauth.account.context_processors.account",
#     "allauth.socialaccount.context_processors.socialaccount",)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            os.path.join(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],

        },
    },
]



AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = 'dashboard'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

#this prevents crash when loading filter_analysis forms.py
# DEBUG_TOOLBAR_PATCH_SETTINGS = True
INTERNAL_IPS = ['127.0.0.1']
# INTERNAL_IPS = ['127.0.0.1']

#django celery settings

CELERY_RESULT_BACKEND = 'django-db'


# celery queues setup
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'



CELERY_ROUTES = {
    'workers.tasks.install_worker': {'queue': 'master'},
    # 'individuals.tasks.AnnotateVariants': {'queue': 'annotation'},
    # 'individuals.tasks.PopulateVariants': {'queue': 'insertion'},
}

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

FILE_UPLOAD_PERMISSIONS = 0o0777


try:
    from .local_settings import *
except ImportError:
    pass

