"""
WSGI config for mendelmd project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

import site
import sys

#site.addsitedir('/projects/venv/lib/python3.5/site-packages')

#site.addsitedir('/projects/mendelmd_master')

#sys.path.append('/projects/venv/lib/python3.5/site-packages')
#sys.path.append('/projects/mendelmd_dev')
#sys.path.append('/home/ubuntu/projects/mendelmdenv/lib/python3.5/site-packages')
#sys.path.append('/home/ubuntu/projects/mendelmd/mendelmd_master')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mendelmd.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
