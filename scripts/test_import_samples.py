import os, sys
import gzip

import json
import os

from subprocess import run

proj_path = '/projects/mendelmd'
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mendelmd.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
# os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from individuals.models import Individual
from files.models import File as Fileobj
from django.contrib.auth.models import User
from django.core.files import File
from django.utils.text import slugify
from individuals.tasks import VerifyVCF
from django.conf import settings

user = User.objects.first()

print(user)

individual = Individual.objects.create(user=user, status='new')
individual.name = 'test sample'
individual.location = 's3://analysis-testdev-results/mendelmd/sample.1000.vcf'
individual.save()

