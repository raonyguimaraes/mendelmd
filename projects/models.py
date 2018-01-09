from django.db import models
from django.contrib.auth.models import User, Group
from individuals.models import Individual
from files.models import File
from tasks.models import Task

# class File(models.Model):

#     user = models.ForeignKey(User, editable=False, null=True, on_delete=models.CASCADE)
    
#     location = models.TextField(null=True, blank=True)
#     name = models.CharField(max_length=30)
#     size = models.BigIntegerField(null=True, blank=True)
#     human_size = models.CharField(max_length=30)

#     status = models.CharField(max_length=30)
#     md5 = models.TextField(null=True, blank=True)
#     creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
#     modified_date = models.DateTimeField(null=True, blank=True)

class Project(models.Model):

    user = models.ForeignKey(User, editable=False, null=True, on_delete=models.CASCADE)
    individuals = models.ManyToManyField(Individual, blank=True)
    
    files = models.ManyToManyField(File, blank=True)
    tasks = models.ManyToManyField(Task, blank=True)

    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    is_public = models.BooleanField(default=False)
    status = models.CharField(max_length=100, blank=True, editable=False)

    paths = models.TextField(null=True, blank=True)

    groups = models.ManyToManyField(Group, editable=True, related_name="project_groups", blank=True)
    members = models.ManyToManyField(User, editable=True, related_name="project_members", blank=True)

    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    