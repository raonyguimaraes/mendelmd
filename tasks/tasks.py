# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from files.models import File
from .models import Task as Taskobj

import urllib.request, os

@shared_task()
def import_project_files_task(project_id):
    print('Import Files on ', project_id)
    # return x + y

def human_size(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    """ Returns a human readable string reprentation of bytes"""
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])

@shared_task()
def check_file(task_id):

    task = Taskobj.objects.get(pk=task_id)

    task.status = 'started'
    task.save()

    manifest = task.manifest
    file_id = manifest['file']
    print('File ID', file_id)

    file = File.objects.get(pk=file_id)
    link = file.location
    print('link', link)
    print('link', link.strip())
    print('link', link.encode())
    

    file.name = os.path.basename(link)
    
    site = urllib.request.urlopen(link)
    file_size = site.info()['Content-Length']
    file.size = int(file_size)
    file.human_size = human_size(int(file_size))
    file.status = 'checked'
    file.save()
    task.status = 'done'
    task.save()

@shared_task()
def download_file(project_file_id):
    file = File.objects.get(pk=project_file_id)
    link = file.location