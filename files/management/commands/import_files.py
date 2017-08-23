from django.core.management.base import BaseCommand, CommandError
from files.models import File, S3Credential
import boto3
from django.conf import settings

class Command(BaseCommand):
    help = 'Import Files'

    def handle(self, *args, **options):
        print('Hello World Import Files')
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
                        # file = File(
                        #     name=key.key,
                        #     size=int(key.size),
                        #     last_modified=str(key.last_modified),
                        # )
                        # file.save()
        self.stdout.write(self.style.SUCCESS('Successfully downloaded files!'))