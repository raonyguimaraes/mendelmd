from django.db import models

from django.urls import reverse

from projects.models import Project
from settings.models import Provider

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

    name = models.CharField(max_length=30)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.ForeignKey(AnalysisType, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('analysis-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

