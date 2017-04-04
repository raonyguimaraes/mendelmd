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

#site.addsitedir('/projects/mendelmd_master/mendelmd_source')

<<<<<<< HEAD
sys.path.append('/projects/venv/lib/python3.5/site-packages')
sys.path.append('/projects/mendelmd_dev/mendelmd_source')
=======
#sys.path.append('/home/ubuntu/projects/mendelmdenv/lib/python3.5/site-packages')
#sys.path.append('/home/ubuntu/projects/mendelmd/mendelmd_master/mendelmd_source')
>>>>>>> 30979687f70ec59207a2aac8c7b36e118561ce5f


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mendelmd.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
