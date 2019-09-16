from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class FilterAnalysis(models.Model):
    name = models.CharField(max_length=255)
    filterstring = models.TextField()
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class FamilyFilterAnalysis(models.Model):
    name = models.CharField(max_length=255)
    filterstring = models.TextField()
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class FilterConfig(models.Model):
    name = models.CharField(max_length=255)
    filterstring = models.TextField()
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    