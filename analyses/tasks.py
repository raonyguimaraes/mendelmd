# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def run_analysis_task(analysis_id):
    print('analysis_id', analysis_id)
    # print('hello!')
