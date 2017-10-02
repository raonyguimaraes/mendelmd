
import os, sys
import gzip

import json
import os
script_dir = os.getcwd()
current_dir = os.getcwd().split('/')
#remove just one path and add mendel,md source

del current_dir[-1]
proj_path = "/".join(current_dir)
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mendelmd.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
# os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from individuals.models import Individual
from django.contrib.auth.models import User
from django.core.files import File
from django.utils.text import slugify
from individuals.tasks import VerifyVCF
from django.conf import settings
# print(args)

individuals = Individual.objects.all()

for individual in individuals:
    print(individual.vcf_file)

    # individual.vcf_file = str(individual.vcf_file).replace('mendelmd_source/', '')
    # print(individual.vcf_file)
    
    # individual.save()


# user = User.objects.first()

# individual.save()

# VerifyVCF.delay(individual.id)