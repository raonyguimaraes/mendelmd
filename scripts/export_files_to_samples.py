
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
from files.models import File
from django.contrib.auth.models import User


individuals = Individual.objects.all()
files = File.objects.all()

for file in files:
    path = os.path.dirname(file.location)+'/'
    print(path)
    individual = Individual.objects.get(vcf_file__icontains=path)
    # for individual in individuals:
    print(individual.name, individual.vcf_file)
    individual.vcf_file = file.location
    individual.save()
    # die()

