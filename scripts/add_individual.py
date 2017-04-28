
import os, sys
import gzip

import json
import os
script_dir = os.getcwd()
current_dir = os.getcwd().split('/')
#remove just one path and add mendel,md
current_dir[-1] = 'mendelmd_source'

proj_path = "/".join(current_dir)
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mendelmd.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from individuals.models import Individual
from django.contrib.auth.models import User
from django.core.files import File
from django.utils.text import slugify
from individuals.tasks import VerifyVCF
from django.conf import settings
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default='input', required=True)
args = parser.parse_args()

# print(args)


individuals = Individual.objects.all()

user = User.objects.first()

print(user)
individual = Individual.objects.create(user=user, status='new')

# filepath = '/home/raony/dev/mendelmd/examples/miller.vcf.gz'
filepath = args.input

filename = os.path.basename(filepath)
dirname = os.path.dirname(filepath)
print(dirname)
print(filename)

command = 'cp %s .' % (filepath)
os.system(command)

if filename.endswith('.gz'):
    file = gzip.open('%s' % (filename))
else:
    file = open('%s' % (filename))

individual.vcf_file = File(file)

# print(individual.vcf_file.file)

command = 'rm %s' % (filename)
os.system(command)

individual.name = str(os.path.splitext(individual.vcf_file.name)[0]).replace('.vcf', '').replace('.gz', '').replace('.rar', '').replace('.zip', '').replace('._', ' ').replace('.', ' ')
individual.save()
os.chmod("%s/genomes/%s/%s" % (settings.BASE_DIR, slugify(individual.user), individual.id), 0o777)

VerifyVCF.delay(individual.id)