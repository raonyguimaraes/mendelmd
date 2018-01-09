from django.contrib.postgres.fields import JSONField
from django.db import models

class Task(models.Model):

	user = models.ForeignKey(User, editable=False, null=True, on_delete=models.CASCADE)
	
	name = models.CharField(max_length=30)
	
	manifest = JSONField()
	
	status = models.CharField(max_length=30)
    md5 = models.TextField(null=True, blank=True)
    
    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name