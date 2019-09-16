from django.db import models

from django.contrib.auth.models import User
from datetime import datetime
from files.models import File
from django.urls import reverse

class Sample(models.Model):
    def get_upload_path(self, filename):
        if self.user != None:
            string = "%s/media/%s/%s/%s" % (settings.BASE_DIR, slugify(self.user.username), self.id, filename)
        else:
            string = "%s/media/public/%s/%s" % (settings.BASE_DIR, self.id, filename)
        return string

    user = models.ForeignKey(User, editable=False, null=True, on_delete=models.CASCADE)
    files = models.ManyToManyField(File, blank=True)

    # shared_with_users = models.ManyToManyField(User, editable=True, related_name="shared_with_users", blank=True)
    # shared_with_groups = models.ManyToManyField(UserGroup, editable=True, related_name="shared_with_groups", blank=True)

    name = models.CharField(max_length=600)
    is_featured = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    
    file = models.FileField(upload_to=get_upload_path, blank=True, help_text="File Format: VCF",max_length=600)
    file_header = models.TextField(null=True, blank=True)

    prefix = models.TextField(null=True, blank=True)


    status = models.CharField(max_length=100, blank=True, editable=False)
    n_variants = models.IntegerField(null=True, blank=True, editable=False)
    n_lines = models.IntegerField(null=True, blank=True, editable=False)

    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        self.modified_date = datetime.now()
        return super(Sample, self).save(*args, **kwargs)


class SampleGroup(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Sample,
        related_name='samplegroup_members')
    def __str__(self):
        return self.name

    
    def get_absolute_url(self):
        return reverse('samplegroup-view', kwargs={'pk': self.pk})

