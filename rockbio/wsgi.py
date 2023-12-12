"""
WSGI config for rockbio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

import site
import sys

#site.addsitedir('/projects/venv/lib/python3.5/site-packages')
#site.addsitedir('/projects/rockbio_master')
#sys.path.append('/projects/venv/lib/python3.5/site-packages')
#sys.path.append('/projects/rockbio_dev')
#sys.path.append('/home/ubuntu/projects/rockbioenv/lib/python3.5/site-packages')
#sys.path.append('/home/ubuntu/projects/rockbio/rockbio_master')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rockbio.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
