from django.db import models


# Create your models here.
class Server(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=30)

    desc = models.TextField(null=True)
    status = models.TextField(null=True)

    usage = models.TextField(null=True)
    
    cpu_load = models.TextField(null=True)
    password = models.TextField(null=True)

    provider = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)