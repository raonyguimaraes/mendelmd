from django.db import models
from django.contrib.auth.models import User, Group
from individuals.models import Individual
from individuals.models import Group as IndividualGroup

import os
from datetime import datetime

from django.utils.text import slugify

class Case(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('solved', 'Solved'),
        ('closed', 'Closed'),
    )
    status = models.CharField(max_length=100,
                                      choices=STATUS_CHOICES,
                                      default='new')
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)

    shared_with_users = models.ManyToManyField(User, related_name='shared_with', blank=True)
    shared_with_groups= models.ManyToManyField(Group, related_name='shared_with', blank=True)

    # individual = models.ForeignKey(Individual)
    name = models.CharField(max_length=600, blank=True)
    description = models.TextField(blank=True, null=True)
    # individuals = models.ManyToManyField(Individual)
   
    mother = models.ForeignKey(Individual, blank=True, related_name='mother', null=True, on_delete=models.CASCADE)
    father = models.ForeignKey(Individual, blank=True, related_name='father', null=True, on_delete=models.CASCADE)

    children = models.ManyToManyField(Individual, blank=True, related_name='children')

    cases = models.ManyToManyField(Individual, blank=True, related_name='cases')

    case_groups = models.ManyToManyField(Group, blank=True, related_name='case_groups', verbose_name="Groups of Cases")

    controls = models.ManyToManyField(Individual, blank=True, related_name='controls', verbose_name="Controls")

    control_groups = models.ManyToManyField(Group, blank=True, related_name='control_groups', verbose_name="Groups of Controls")
    

    # mother = models.ManyToManyField(Individual, related_name='mother')
    # children = models.ManyToManyField(Individual, related_name='children')


# class AnnotationCase(models.Model):
#   case=models.ForeignKey(Case)
#   annotation = models.TextField(blank=True)


    # 
    
    # featured = models.BooleanField(default=True)
    # variants_file = models.FileField(upload_to=get_upload_path, blank=True, help_text="File Format: VCF",max_length=600)
    
    # status = models.CharField(max_length=100, blank=True, editable=False)
    # n_records = models.IntegerField(blank=True, editable=False)
    # n_lines = models.IntegerField(blank=True, editable=False)
    
    # user = models.ForeignKey(User, editable=False)

    # creation_date = models.DateTimeField(auto_now_add=True,blank=True)
    # modified_date = models.DateTimeField(blank=True)

    # annotation_time = models.TextField(blank=True)
    # insertion_time = models.TextField(blank=True)

    # insertion_time_mongo = models.TextField(blank=True)

    # def __unicode__(self):
    #   return self.name

    # @models.permalink
    # def get_absolute_url(self):
    #   return ('individual-new',)

    # def __unicode__(self):
    #     return self.name

    # def save(self, *args, **kwargs):
    #     if not self.creation_date:
    #         self.creation_date = datetime.now()
    #     self.modified_date = datetime.now()
    #     return super(Individual, self).save(*args, **kwargs)


    # def delete(self, *args, **kwargs):
    #     super(Individual, self).delete(*args, **kwargs)

# class IndividualSummary(models.Model):
#     individual = models.ForeignKey(Individual)
#     ann_name = models.CharField(max_length=600)
#     ann_value = models.CharField(max_length=600)



# class IndividualMedicalConditionVariant(models.Model):
#     individual_variant = models.ForeignKey(Variant)
#     snp = models.ForeignKey(Snp)    
    
# class IndividualMedicalCondition(models.Model):
#     individual = models.ForeignKey(Individual)
#     medical_condition = models.ForeignKey(MedicalCondition)
#     variants = models.ManyToManyField(IndividualMedicalConditionVariant)
#     max_magnitude = models.FloatField(blank=True)
    
# class IndividualMedicineVariant(models.Model):
#     individual_variant = models.ForeignKey(Variant)
#     snp = models.ForeignKey(Snp)    
    
# class IndividualMedicine(models.Model):
#     individual = models.ForeignKey(Individual)
#     medicine = models.ForeignKey(Medicine)
#     variants = models.ManyToManyField(IndividualMedicineVariant)
#     max_magnitude = models.FloatField(blank=True)

# class IndividualHGMDMutation(models.Model):
#     individual = models.ForeignKey(Individual)
#     individual_variant = models.ForeignKey(Variant)
#     hgmdmutation = models.ForeignKey(HGMDMutation)


# class Group(models.Model):
#     name = models.CharField(max_length=128)
#     members = models.ManyToManyField(Individual)

#     def __unicode__(self):
#         return self.name

# class Relationship(models.Model):
#   group = models.ForeignKey(Group)
#   first_person = models.ForeignKey(Individual, related_name='first')
#   second_person = models.ForeignKey(Individual, related_name='second')
    
    
    
