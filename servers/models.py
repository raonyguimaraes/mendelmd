from django.db import models

from apps.models import WebApp
import socket

# Create your models here.
class Server(models.Model):
    def __str__(self):
        return self.name

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Server._meta.fields]

    name = models.CharField(max_length=30)
    url = models.CharField(max_length=30,null=True,blank=True)
    username = models.CharField(max_length=300,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    cost = models.FloatField(null=True,blank=True,default=0)
    desc = models.CharField(max_length=300,null=True,blank=True)
    status = models.CharField(max_length=300,null=True,blank=True)
    usage = models.CharField(max_length=300,null=True,blank=True)
    cpu_load = models.CharField(max_length=300,null=True,blank=True)
    provider = models.CharField(max_length=300,null=True,blank=True)
    ip = models.CharField(max_length=300,null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.url:
            self.ip=socket.gethostbyname(self.url)
        super(Server, self).save(*args, **kwargs)
    # apps = models.ManyToManyField(WebApp)