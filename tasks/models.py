from django.db import models
from django.contrib.auth.models import User
from individuals.models import Individual
# Create your models here.

class Task(models.Model):

    user = models.ForeignKey(User, editable=False, null=True)

    individuals = models.ManyToManyField(Individual)

    name = models.CharField(max_length=600)
    status = models.CharField(max_length=600)
    machine = models.CharField(max_length=600)
    type = models.CharField(max_length=600)
    retry = models.IntegerField(default = 0)
    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    execution_time = models.TimeField(null=True)

