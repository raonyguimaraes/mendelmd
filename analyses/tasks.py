# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task()
def test_task(project_file_id):
    print('Hello')