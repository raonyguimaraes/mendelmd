from .models import S3Credential
import boto3

def import_files():
    credentials = S3Credential.objects.all()
    for credential in credentials:
        print(credential)