from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

class S3Credential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=255)
    access_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    buckets = models.TextField(null=True, blank=True)
    exclude_paths= models.TextField(null=True, blank=True)
    exclude_files = models.TextField(null=True, blank=True)
