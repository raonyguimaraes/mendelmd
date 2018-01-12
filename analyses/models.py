from django.db import models

from django.urls import reverse

class Analysis(models.Model):
    name = models.CharField(max_length=30)

    def get_absolute_url(self):
        return reverse('analysis-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name