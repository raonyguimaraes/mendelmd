from django.db import models
from django.contrib.auth.models import User, Group
from individuals.models import Individual
from files.models import File
# Create your models here.

class Project(models.Model):
    # class Meta:
    #     app_label = 'projects'

    user = models.ForeignKey(User, editable=False, null=True, on_delete=models.CASCADE)
    individuals = models.ManyToManyField(Individual, blank=True)
    files = models.ManyToManyField(File, blank=True)

    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    is_public = models.BooleanField(default=False)
    status = models.CharField(max_length=100, blank=True, editable=False)

    groups = models.ManyToManyField(Group, editable=True, related_name="project_groups", blank=True)
    members = models.ManyToManyField(User, editable=True, related_name="project_members", blank=True)

    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)

