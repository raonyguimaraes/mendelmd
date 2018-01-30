from django.core.management.base import BaseCommand, CommandError
from files.models import File
from settings.models import S3Credential
import boto3
import os
from django.conf import settings
import time

class Command(BaseCommand):
    help = 'Import Files'

    def handle(self, *args, **options):
        print('Hello World Import Files')
        start_time = time.time()

        self.download_files()
        self.import_files()
        elapsed_time = time.time() - start_time
        print('Importing Files Took {}'.format(elapsed_time))
    def download_files(self):
        print('Download Files')
        file_list = open('%s/data/files/all_files.txt' % (settings.BASE_DIR), 'w')
        s3credentials = S3Credential.objects.all()
        for s3credential in s3credentials:
            print(s3credential.name)
            for bucket_name in s3credential.buckets.splitlines():
                session = boto3.Session(
                    aws_access_key_id=s3credential.access_key,
                    aws_secret_access_key=s3credential.secret_key
                )
                s3 = session.resource('s3')
                bucket = s3.Bucket(bucket_name)
                print(bucket)
                for key in bucket.objects.all():
                    if key.size != 0:
                        file = [str(key.last_modified), str(key.size), bucket.name, key.key]
                        file_list.writelines('%s\n' % ('\t'.join(file)))
        self.stdout.write(self.style.SUCCESS('Successfully downloaded files!'))

    def import_files(self):
        print('Import Files')
        File.objects.all().delete()
        file_list = open('%s/data/files/all_files.txt' % (settings.BASE_DIR))
        file_types = {}
        files = {}
        exclude_paths = []
        s3credentials = S3Credential.objects.all()
        for s3credential in s3credentials:
            # print()
            # print(s3credential.exclude_paths.splitlines())
            for item in s3credential.exclude_paths.splitlines():
                exclude_paths.append(item)

        n_files = 0
        for line in file_list:
            row = line.strip().split('\t')
            file = {
                'date': row[0],
                'size': row[1],
                'bucket': row[2],
                'location': row[3],
            }
            if not file['location'].startswith(tuple(exclude_paths)):
                full_path = 's3://' + file['bucket'] + '/' + file['location']
                n_files += 1
                file_name, file_extension = os.path.splitext(file['location'])
                if file_extension == '.gz':
                    file_name, file_extension = os.path.splitext(file_name)
                file['extension'] = file_extension
                if file_extension not in file_types:
                    file_types[file_extension] = []
                file_types[file_extension].append(full_path)
                files[full_path] = file
        #
        # print(n_files)
        print('Summary')
        print('Number of files: {}'.format(n_files))
        print('Number of file types: {}'.format(len(file_types)))
        extensions = ['.fastq', '.bam', '.vcf']
        file_objs = []
        for extension in extensions:
            for file in file_types[extension]:
                # print(file)


                file_name, file_extension = os.path.splitext(file)
                if file_extension == '.gz':
                    file_name, file_extension = os.path.splitext(file_name)
                basename = os.path.basename(file_name)

                file_obj = File(
                    name=basename,
                    size=files[file]['size'],
                    last_modified=str(files[file]['date']),
                    file_type=file_extension.replace('.', ''),
                    location=file,
                )
                #print(file_obj,files[file])
                file_objs.append(file_obj)
                #file_obj.save()
        File.objects.bulk_create(file_objs)
