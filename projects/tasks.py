# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import File

import urllib.request, os

@shared_task()
def import_project_files_task(project_id):
    print('Import Files on ', project_id)
    # return x + y

def human_size(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    """ Returns a human readable string reprentation of bytes"""
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])

@shared_task()
def check_file(project_file_id):
	file = File.objects.get(pk=project_file_id)
	link = file.location
	
	file.name = os.path.basename(link)

	site = urllib.request.urlopen(link)
	file_size = site.info()['Content-Length']
	file.size = int(file_size)
	file.human_size = human_size(int(file_size))
	file.status = 'checked'
	file.save()

@shared_task()
def download_file(project_file_id):
	file = File.objects.get(pk=project_file_id)
	link = file.location