from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from files.models import File
# from analyses.models import Analysis

class Task(models.Model):

    user = models.ForeignKey(User, editable=False, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    manifest = JSONField()
    
    status = models.CharField(max_length=30)
    action = models.CharField(max_length=30)
    md5 = models.TextField(null=True, blank=True)

    output = models.TextField(null=True, blank=True)
    
    started = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)
    timetaken = models.DateTimeField(null=True, blank=True)
    
    total_cost = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=10)

    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    files = models.ManyToManyField(File)

    def __str__(self):
        return self.name
