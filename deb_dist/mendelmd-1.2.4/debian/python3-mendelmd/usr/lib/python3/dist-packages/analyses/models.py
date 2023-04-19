from django.db import models

from django.urls import reverse

from projects.models import Project
from settings.models import Provider
from samples.models import Sample
from tasks.models import Task
from files.models import File
from mapps.models import App as Mapp

from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import JSONField

class AnalysisType(models.Model):
    class Meta:
        verbose_name_plural = "analysis_types"

    name = models.CharField(max_length=30)
    repository = models.CharField(max_length=600, null=True, blank=True)
    def __str__(self):
        return self.name


class Analysis(models.Model):
    class Meta:
        verbose_name_plural = "analyses"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    params = JSONField(null=True, blank=True)

    name = models.CharField(max_length=30)
    status = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    apps = models.ManyToManyField(Mapp)
    samples = models.ManyToManyField(Sample)
    tasks = models.ManyToManyField(Task)
    files = models.ManyToManyField(File)

    # type = models.ForeignKey(AnalysisType, on_delete=models.CASCADE)
    # provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('analysis-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

