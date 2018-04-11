from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

# Create your models here.

class App(models.Model):
    def get_absolute_url(self):
        return "/apps/"

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    source = models.CharField(max_length=600, null=True, blank=True)
    repository = models.CharField(max_length=600, null=True, blank=True)
    install = models.CharField(max_length=600, null=True, blank=True)
    main = models.CharField(max_length=600, null=True, blank=True)
    type = models.CharField(max_length=255)
    config = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
