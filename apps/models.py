# Create your models here.
from django.db import models


# Create your models here.
class WebApp(models.Model):
    def __str__(self):
        return self.name
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in WebApp._meta.fields]

    name = models.CharField(max_length=30)
    
    data = models.JSONField(null=True,blank=True)

    server = models.TextField(null=True,blank=True)
    
    desc = models.TextField(null=True,blank=True)
    status = models.TextField(null=True,blank=True)

    # usage = models.TextField(null=True)
    
    # cpu_load = models.TextField(null=True)
    # password = models.TextField(null=True)

    # provider = models.CharField(max_length=30)
    # ip = models.CharField(max_length=30)
