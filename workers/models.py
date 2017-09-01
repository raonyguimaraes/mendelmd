from django.db import models

# Create your models here.

class Worker(models.Model):

    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    worker_id = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    execution_time = models.TimeField(null=True)