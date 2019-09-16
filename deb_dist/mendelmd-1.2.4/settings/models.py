from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class S3Credential(models.Model):
    def get_absolute_url(self):
        return "/settings/"
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=255)
    access_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    buckets = models.TextField(null=True, blank=True)
    exclude_paths= models.TextField(null=True, blank=True)
    exclude_files = models.TextField(null=True, blank=True)

class Provider(models.Model):
    def get_absolute_url(self):
        return "/settings/"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    config = JSONField()
    def __str__(self):
        return self.name

class Subnet(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=255)
    config = JSONField()
    count = models.IntegerField(null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True,
        )
    params = JSONField()