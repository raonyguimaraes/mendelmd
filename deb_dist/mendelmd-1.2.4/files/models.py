from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.contrib.postgres.fields import JSONField

# Create your models here.
class File(models.Model):

    def get_upload_path(self, filename):
        if self.user != None:
            string = "%s/media/%s/%s/%s" % (settings.BASE_DIR, slugify(self.user.username), self.id, filename)
        else:
            string = "%s/media/public/%s/%s" % (settings.BASE_DIR, self.id, filename)
        return string

    def get_absolute_url(self):
        return "/files/"

    def __str__(self):
        return self.name

    user = models.ForeignKey(User, editable=False, null=True, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=600, blank=True)
    
    size = models.BigIntegerField(null=True, blank=True)
    
    file_type = models.TextField(null=True, blank=True)
    extension = models.TextField(null=True, blank=True)

    location = models.TextField(null=True, blank=True)    
    local_file = models.FileField(upload_to=get_upload_path, blank=True, help_text="File Format: VCF",max_length=600)
    remote_location = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    
    status = models.TextField(null=True, blank=True)
    last_output = models.TextField(null=True, blank=True)
    params = JSONField(null=True, blank=True)

    md5 = models.TextField(null=True, blank=True)

    last_modified = models.DateTimeField(null=True, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
