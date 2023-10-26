# Create your models here.


from django.db import models


class SSHKey(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=30)
    key = models.TextField()


class CloudKey(models.Model):
    def __str__(self):
        return self.name

    CLOUDPROVIDERS = [
        ("Hetzner", "Hetzner"),
        ("Google", "Google"),
        ("AWS", "AWS"),
        ("Cpanel", "Cpanel"),
    ]
    name = models.CharField(max_length=30)
    key = models.TextField(blank=True)
    host = models.CharField(max_length=200,blank=True)
    username = models.CharField(max_length=200,blank=True)
    password = models.CharField(max_length=200,blank=True)
    cloudprovider = models.CharField(max_length=30, choices=CLOUDPROVIDERS)
