from django.db import models

# Create your models here.
class Disease(models.Model):
    name = models.CharField(max_length=255)
    omim_id = models.CharField(max_length=255)
    chr_location = models.CharField(max_length=255)
    gene_names = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Gene(models.Model):
    official_name = models.CharField(max_length=255)
    chromossome = models.CharField(max_length=255, null=True, blank=True)
    names = models.TextField(null=True, blank=True)
    strand = models.CharField(max_length=255, null=True, blank=True)
    chr_location = models.CharField(max_length=255, null=True, blank=True)
    transcription_start = models.IntegerField(null=True, blank=True)
    transcription_end = models.IntegerField(null=True, blank=True)
    cds_start = models.IntegerField(null=True, blank=True)
    cds_end = models.IntegerField(null=True, blank=True)
    exons_count = models.CharField(max_length=500, null=True, blank=True)
    exons_start = models.TextField(null=True, blank=True)
    exons_end = models.TextField(null=True, blank=True)
    diseases = models.ManyToManyField(Disease)


class HGMDPhenotype(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
 

class HGMDGene(models.Model):
    symbol = models.CharField(max_length=255)
    aliases = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    description_aliases = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    n_mutations = models.IntegerField(null=True, blank=True)
    diseases = models.ManyToManyField(HGMDPhenotype)


#missense/nonsense   splicing    regulatory  small deletions small insertions    small indels    
#gross deletions gross insertions    complex rearrangements  repeat variations



class HGMDMutation(models.Model):
    
    gene = models.ForeignKey(HGMDGene, on_delete=models.CASCADE)

    mutation_type = models.CharField(max_length=255, null=True, blank=True)
    acession = models.CharField(max_length=255, null=True, blank=True)
    
    phenotype = models.ForeignKey(HGMDPhenotype, on_delete=models.CASCADE)
    reference = models.TextField(null=True, blank=True)
    extras = models.TextField(null=True, blank=True)

    rsid = models.CharField(max_length=255, null=True, blank=True)
    dm_mutation = models.BooleanField(default=False)
    coordinate = models.CharField(max_length=100, null=True, blank=True)
    chromossome = models.CharField(max_length=100, null=True, blank=True)

    position = models.CharField(max_length=100, null=True, blank=True)
    #misense
    codon_change = models.CharField(max_length=255, null=True, blank=True)
    aa_change = models.CharField(max_length=255, null=True, blank=True)
    hgvs_nucleotide = models.CharField(max_length=100, null=True, blank=True)
    hgvs_protein = models.CharField(max_length=100, null=True, blank=True)
    #splicing
    splicing_mutation = models.CharField(max_length=255, null=True, blank=True)
    #regulatory
    regulatory_sequence = models.TextField(null=True, blank=True)
    #small deletions
    deletion_sequence = models.TextField(null=True, blank=True)
    #small insertions
    insertion_sequence = models.TextField(null=True, blank=True)

    #gross deletions
    dna_level = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    #Gross insertions 
    insertion_duplication = models.CharField(max_length=255, null=True, blank=True)
    #Repeat variations
    amplified_sequence = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    normal_range = models.CharField(max_length=255, null=True, blank=True)
    pathological_range = models.CharField(max_length=255, null=True, blank=True)

    def get_fields(self):
         return [(field, field.value_to_string(self)) for field in HGMDMutation._meta.fields]


    
    
