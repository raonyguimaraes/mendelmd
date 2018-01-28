
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

for individual in individuals:
    print(individual)
    print(individual.vcf_file)

    file = File(user=individual.user)
    file.location = individual.vcf_file
    file.save()

    # user = models.ForeignKey(User, editable=False, null=True, on_delete=models.CASCADE)

    # shared_with_users = models.ManyToManyField(User, editable=True, related_name="shared_with_users", blank=True)
    # shared_with_groups = models.ManyToManyField(UserGroup, editable=True, related_name="shared_with_groups", blank=True)

    # name = models.CharField(max_length=600)
    # is_featured = models.BooleanField(default=True)
    # is_public = models.BooleanField(default=False)
    # vcf_file = models.FileField(upload_to=get_upload_path, blank=True, help_text="File Format: VCF",max_length=600)
    # vcf_header = models.TextField(null=True, blank=True)
    # status = models.CharField(max_length=100, blank=True, editable=False)
    # n_variants = models.IntegerField(null=True, blank=True, editable=False)
    # n_lines = models.IntegerField(null=True, blank=True, editable=False)

    # creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    # modified_date = models.DateTimeField(null=True, blank=True)

    # annotation_time = models.CharField(max_length=200, null=True, blank=True)
    # insertion_time = models.CharField(max_length=200, null=True, blank=True)
    