# -*- coding: utf-8 -*-

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task()
def import_project_files_task(project_id):
    print('Import Files on ', project_id)
    # return x + y



# app = Celery('tasks', broker='pyamqp://guest@localhost//')


# def add(x, y):
#     return x + y
