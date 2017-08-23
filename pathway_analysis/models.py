from django.db import models

# Create your models here.
class Pathway(models.Model):
    kegg = models.CharField(max_length=255)
    name = models.TextField(null=True, blank=True)
    genes = models.TextField(null=True, blank=True)

#GenePathway