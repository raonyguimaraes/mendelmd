# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .models import Project, ProjectFile, ProjectSample 
from settings.models import S3Credential
import boto3


@shared_task
def import_project_files_task(project_id):
    print('project', project_id)
    project = Project.objects.get(pk=project_id)
    samples = ProjectSample.objects.filter(project=project)
    files = ProjectFile.objects.filter(project=project)
    # print(samples)
    for sample in samples:
        sample.n_files = 0
        sample.n_fastqs = 0
        sample.n_bams = 0
        sample.n_vcfs = 0
        sample.files.clear()
        #get all files from location
        if sample.location != '':
            for file in files:
                add_file = False
                location = file.location
                if sample.location in file.location:
                    if sample.prefix != '':
                        if sample.prefix in file.location:
                            add_file = True
                    else:
                        add_file = True
                    if add_file:
                        sample.files.add(file)
                        sample.n_files += 1
                        if location.endswith('.fq.gz') or location.endswith('.fastq.gz'):
                            sample.n_fastqs += 1
                        if location.endswith('.bam'):
                            sample.n_bams += 1
                        if location.endswith('.vcf.gz') or location.endswith('.vcf'):
                            sample.n_vcfs += 1
        sample.save()
        #match if prefix is available
        #add them all to sample
        #save and be happy :D
