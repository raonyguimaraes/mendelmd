from django.db import models
from django.conf import settings

# Create your models here.
class File(models.Model):

    def get_upload_path(self, filename):
        string = "%s/upload/%s/%s" % (settings.BASE_DIR, self.id, filename)
        return string
    name = models.TextField(max_length=50)
    size = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    file_type = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    local_file = models.FileField(upload_to=get_upload_path, blank=True, help_text="File Format: VCF",max_length=600)
    status = models.TextField(null=True, blank=True)
    md5 = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)

class S3Credential(models.Model):
    def get_absolute_url(self):
        return "/files/settings/"
    name = models.CharField(max_length=255)
    access_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    buckets = models.TextField(null=True, blank=True)
