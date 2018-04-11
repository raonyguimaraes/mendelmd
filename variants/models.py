from django.db import models
from samples.models import Sample

class Variant(models.Model):

    pos_index = models.TextField(db_index=True)#ex. 1-326754756
    index = models.TextField(db_index=True)#ex. 1-326754756-326754756-G-T
    chr = models.TextField(verbose_name="Chr", db_index=True)
    start = models.IntegerField(db_index=True)
    end = models.IntegerField(db_index=True)
    variant_id = models.TextField(verbose_name="ID", db_index=True)
    ref = models.TextField(null=True, blank=True, db_index=True)
    alt = models.TextField(null=True, blank=True, db_index=True)
    def get_fields(self):
        return [(field.name, field.verbose_name.title().replace('_', ' ')) for field in Variant._meta.fields]

class VariantIndex(models.Model):
    index = models.TextField()#ex. 1-2387623-G-T REF ALT for each REF and ALT
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)

class Genotype(models.Model):
    genotype = models.TextField(null=True, blank=True)

class SampleVariantGenotype(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    genotype = models.ForeignKey(Genotype, on_delete=models.CASCADE)