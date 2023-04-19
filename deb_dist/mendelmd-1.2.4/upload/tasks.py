# -*- coding: utf-8 -*-

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

# from celery.task import Task
# from celery.registry import tasks
from django.db import transaction
from django.core.files import File
# from celery import task

from individuals.models import *

from variants.models import *

# from mysql_bulk_insert import bulk_insert
from django.shortcuts import render, get_object_or_404
import os
import datetime
from django.core.mail import send_mail
# from snpedia.models import *
from diseases.models import HGMDMutation
from django.conf import settings

import zipfile
import gzip
import pickle
import tarfile
from collections import OrderedDict


import json
import vcf

from datetime import timedelta
from django.template.defaultfilters import slugify


@shared_task()
def test():
    print("Running periodic task!")
    individuals = Individual.objects.filter(user=None)
    for individual in individuals:
        time_difference = datetime.datetime.now()-individual.creation_date
        if time_difference.days > 0:
            #delete individuals
            os.system('rm -rf %s/genomes/public/%s' % (settings.BASE_DIR, individual_id))
            individual.delete()

