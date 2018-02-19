# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from tasks.models import Task
from .models import Analysis
from samples.models import Sample, SampleGroup

from celery import Celery
app = Celery('mendelmd')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(queue="master")
def create_analysis_tasks(analysis_id):
    print('analysis_id', analysis_id)
    # samples = []
    # print('hello!')
    #create analysis tasks
    # analysis = Analysis.objects.()
    analysis = Analysis.objects.get(pk=analysis_id)
    print(dir(analysis))
    params = analysis.params
    files = params['files']
    for file in files:
        task = Task(user=analysis.user)
        task.manifest = {}
        task.manifest['files'] = [file]
        task.manifest['analysis_types'] = params['analysis_types']
        task.status = 'new'
        task.analysis = analysis
        task.action = 'analysis'
        task.save()
        analysis.tasks.add(task)

    # if 'sample_groups' in  params:
    #     samples = Sample.objects.filter(samplegroup_members__in=params['sample_groups'])
    #     # sample = Sample.objects.first()
    #     # print(dir(sample))
    # for sample in samples:      
    #     print(sample)
    #     for file in sample.files.all():
    #         bam_size = 9223372036854775807
    #         if file.extension == 'bam':
    #             if file.size < bam_size:
    #                 bamfile = file
    #                 bam_size = file.size
    #     print('small bam', bamfile.size)
    # get smallest bam file