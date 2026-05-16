"""
Django settings for mendelmd project.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError('SECRET_KEY environment variable is required')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'


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
    
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'crispy_bootstrap3',
    'django_select2',

    # 'djcelery',
    'celery',
    'django_celery_results',
    # 'kombu.transport.django',
    # 'django_celery_results',
    # 'django_celery_beat',

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
    'stats',
    'databases',
    'projects',
    'files',
    'samples',
    'upload',
    'settings',
    'tasks',
    'workers',
    'analyses',
    'formtools',
    # 'mapps',
    'django_gravatar',    
    #'storages',
    'keys',
    'servers',
    'apps',
    'djstripe',
    'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'mendelmd.urls'

WSGI_APPLICATION = 'mendelmd.wsgi.application'

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': 'mendelmd.db',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
# TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = False

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'



STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


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
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Required by allauth template tags
                'mendelmd.context_processors.stripe',
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

LOGIN_REDIRECT_URL = '/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap3"
CRISPY_TEMPLATE_PACK = 'bootstrap3'





INTERNAL_IPS = ['127.0.0.1']

# new celery 4 config
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
# CELERY_RESULT_EXTENDED = True
CELERY_IMPORTS = ('analyses.tasks','tasks.tasks','workers.tasks','individuals.tasks')

CELERYBEAT_SCHEDULE = {
    'check_queue': {
        'task': 'workers.tasks.check_queue',
        'schedule': 30.0,
    },
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

if 'USE_DOCKER' in os.environ:
    try:
        from .local_settings_docker import *
    except ImportError:
        pass
else:
    try:
        from .local_settings import *
    except ImportError:
        pass

FILE_UPLOAD_PERMISSIONS = 0o644
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000

# ALL AUTH
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS={"username", "email"}
ACCOUNT_SESSION_REMEMBER=True
#ACCOUNT_UNIQUE_EMAIL=True
SOCIALACCOUNT_AUTO_SIGNUP=True
SOCIALACCOUNT_QUERY_EMAIL=True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "")
STRIPE_LIVE_MODE = False
DJSTRIPE_WEBHOOK_SECRET = os.environ.get("DJSTRIPE_WEBHOOK_SECRET", "")

DJSTRIPE_FOREIGN_KEY_TO_FIELD = 'id'
