from django.db import models

from django.contrib.auth.models import User

from datetime import datetime

from django.utils.text import slugify

from django.conf import settings

from django.template.defaultfilters import slugify

# Subclass AbstractUser
class UserGroup(models.Model):
    name = models.CharField(max_length=600)
    members = models.ManyToManyField(User, editable=True, related_name="members", blank=True)
    def __str__(self):
        return self.name


class Individual(models.Model):
    def get_upload_path(self, filename):
        if self.user != None:
            string = "genomes/%s/%s/%s" % (slugify(self.user.username), self.id, filename)#.replace(' ', '_')
        else:
            string = "genomes/public/%s/%s" % (self.id, filename)#.replace(' ', '_')
            print('string',string)
        return string
    user = models.ForeignKey(User, editable=False, null=True, on_delete=models.CASCADE)

    shared_with_users = models.ManyToManyField(User, editable=True, related_name="shared_with_users", blank=True)
    shared_with_groups = models.ManyToManyField(UserGroup, editable=True, related_name="shared_with_groups", blank=True)

    name = models.CharField(max_length=600)
    is_featured = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    vcf_file = models.FileField(upload_to=get_upload_path, blank=True, help_text="File Format: VCF",max_length=600)
    vcf_header = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, blank=True, editable=False)
    n_variants = models.IntegerField(null=True, blank=True, editable=False)
    n_lines = models.IntegerField(null=True, blank=True, editable=False)

    creation_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)

    annotation_time = models.CharField(max_length=200, null=True, blank=True)
    insertion_time = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    # @models.permalink
    # def get_absolute_url(self):
    # 	return ('individual-new',)


    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        self.modified_date = datetime.now()
        return super(Individual, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     super(Individual, self).delete(*args, **kwargs)

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Individual,
        related_name='group_members')
    def __str__(self):
        return self.name

#from individuals.tasks import PopulateControls

class ControlGroup(models.Model):
    def get_upload_path(self, filename):
        string = "upload/controls/%s/%s" % (self.id, filename)#.replace(' ', '_')
        return string
    name = models.CharField(max_length=600)
    vcf_file = models.FileField(upload_to=get_upload_path, blank=True, help_text="File Format: VCF",max_length=600)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        #populate
        #return
        super(ControlGroup, self).save(*args, **kwargs)
        PopulateControls.delay(self.id)


class ControlVariant(models.Model):

    controlgroup = models.ForeignKey(ControlGroup, on_delete=models.CASCADE)
    index = models.TextField(db_index=True)#ex. 1-2387623-G-T
