from settings.models import S3Credential
import boto3
from celery import shared_task
from tasks.models import Task
from .models import File
from subprocess import check_output
import os

@shared_task()
def check_file(task_id):
    task = Task.objects.get(pk=task_id)

    task.status = 'started'
    task.save()

    manifest = task.manifest
    file_id = manifest['file']
    print('File ID', file_id)

    file = File.objects.get(pk=file_id)

    if file.location.startswith('ftp://'):
        print('ftp')
        print(file.location)

     
        file.name = os.path.basename(file.location)

        command = 'curl -sI {} | grep Content-Length'.format(file.location)
        output = check_output(command, shell=True)

        # print()
        size = output.split()[1]

        file.size = int(size)
        # file.human_size = human_size(file.size)



    elif file.location.startswith('http'):
        link = file.location
        print('link', link)
        print('link', link.strip())
        print('link', link.encode())

        file.name = os.path.basename(link)
        
        site = urllib.request.urlopen(link)
        file_size = site.info()['Content-Length']
        file.size = int(file_size)
        # file.human_size = human_size(int(file_size))
        
    elif file.location.startswith('/'):

        path = '/'.join(file.location.split('/')[:-1])

        command = 'ls -lah {}'.format(path)
        output = check_output(command, shell=True)
        file.last_output = output.decode('utf-8')

        filename, file_extension = os.path.splitext(file.location)

        if file_extension in ['.gz', '.zip', '.rar', 'bz2', '.7z']:
            compression = file_extension
            filename, file_extension  = os.path.splitext(filename)
            file_extension += compression

        file.extension = file_extension

        command = 'file {}'.format(file.location)
        output = check_output(command, shell=True)
        file.file_type = ' '.join(output.decode('utf-8').strip().split(' ')[1:])

        file.name = os.path.basename(file.location)
        # print(os.stat(file.location))
        # print(os.path.getsize(file.location))
        file.size = int(os.path.getsize(file.location))

    print('File Name', file.name)
    file.status = 'checked'
    file.save()

    if file.extension == '.vcf.gz' or file.extension == '.vcf':

        task_manifest = {}
        task_manifest['file'] = file.id
        task_manifest['action'] = 'import_vcf'
        
        import_task = Task()
        import_task.manifest = task_manifest
        import_task.status = 'new'
        import_task.action = 'import_vcf'
        import_task.save()
        import_vcf.delay(task.id)

    task.status = 'done'
    task.save()


@shared_task()
def import_vcf(task_id):
    print('importing a vcf file into the database')
    print(task_id)
    task = Task.objects.get(pk=task_id)

    task.status = 'started'
    task.save()
    
    #get vcf
    #get number of samples
    #create samples objects
    #add samples
    #add variants
    #add genotypes
    #kick annotation

