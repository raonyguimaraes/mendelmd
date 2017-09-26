from django.db import models

from diseases.models import Disease
from django.contrib.auth.models import User


# Create your models here.
class Gene(models.Model):

    hgnc_id = models.TextField(blank=True)
    symbol = models.TextField(blank=True)
    name = models.TextField(blank=True)
    locus_group = models.TextField(blank=True)
    locus_type = models.TextField(blank=True)
    status = models.TextField(blank=True)
    location = models.TextField(blank=True)
    location_sortable = models.TextField(blank=True)
    alias_symbol = models.TextField(blank=True)
    alias_name = models.TextField(blank=True)
    prev_symbol = models.TextField(blank=True)
    prev_name = models.TextField(blank=True)
    gene_family = models.TextField(blank=True)
    gene_family_id = models.TextField(blank=True)
    date_approved_reserved = models.TextField(blank=True)
    date_symbol_changed = models.TextField(blank=True)
    date_name_changed = models.TextField(blank=True)
    date_modified = models.TextField(blank=True)
    entrez_id = models.TextField(blank=True)
    ensembl_gene_id = models.TextField(blank=True)
    vega_id = models.TextField(blank=True)
    ucsc_id = models.TextField(blank=True)
    ena = models.TextField(blank=True)
    refseq_accession = models.TextField(blank=True)
    ccds_id = models.TextField(blank=True)
    uniprot_ids = models.TextField(blank=True)
    pubmed_id = models.TextField(blank=True)
    mgd_id = models.TextField(blank=True)
    rgd_id = models.TextField(blank=True)
    lsdb = models.TextField(blank=True)
    cosmic = models.TextField(blank=True)
    omim_id = models.TextField(blank=True)
    mirbase = models.TextField(blank=True)
    homeodb = models.TextField(blank=True)
    snornabase = models.TextField(blank=True)
    bioparadigms_slc = models.TextField(blank=True)
    orphanet = models.TextField(blank=True)
    pseudogene_org = models.TextField(blank=True)
    horde_id = models.TextField(blank=True)
    merops = models.TextField(blank=True)
    imgt = models.TextField(blank=True)
    iuphar = models.TextField(blank=True)
    kznf_gene_catalog = models.TextField(blank=True)
    mamit_trnadb = models.TextField(blank=True)
    cd = models.TextField(blank=True)
    lncrnadb = models.TextField(blank=True)
    enzyme_id = models.TextField(blank=True)
    intermediate_filament_db = models.TextField(blank=True)

    diseases = models.ManyToManyField(Disease, related_name='+')
    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Gene._meta.fields]
    
    
class GeneCategory(models.Model):
    domain = models.CharField(max_length=255, blank=True)
    name = models.TextField(blank=True)
    go = models.CharField(max_length=255)
    definition = models.TextField(blank=True)
    genes = models.ManyToManyField(Gene)
    
    
class Membership(models.Model):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    group = models.ForeignKey(GeneCategory, on_delete=models.CASCADE)
    
    
class GeneGroup(models.Model):
    name = models.CharField(max_length=255)
    genes = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
        
        
class GoTerm(models.Model):
    goid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    namespace = models.CharField(max_length=255)
    parents = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='parents_go')
    children = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='children_go')
    level = models.CharField(max_length=255) 
    is_obsolete = models.BooleanField(default=True)
    alt_ids = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name



class Manifestation(models.Model):
    name = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Intervention(models.Model):
    name = models.TextField(blank=True)

    def __str__(self):
        return self.name    


class CGDCondition(models.Model):
    name = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CGDEntry(models.Model):

    GENE = models.TextField(blank=True)
    HGNC_ID = models.TextField(blank=True)

    ENTREZ_GENE_ID = models.TextField(blank=True)
    CONDITIONS = models.ManyToManyField(CGDCondition, blank=True)
    INHERITANCE = models.TextField(blank=True)
    AGE_GROUP = models.TextField(blank=True)
    ALLELIC_CONDITIONS = models.TextField(blank=True)

    COMMENTS = models.TextField(blank=True)
    INTERVENTION_RATIONALE = models.TextField(blank=True)
    REFERENCES = models.TextField(blank=True)


    MANIFESTATION_CATEGORIES = models.ManyToManyField(Manifestation, blank=True)

    INTERVENTION_CATEGORIES = models.ManyToManyField(Intervention, blank=True)

    def __str__(self):
        return self.GENE

class GeneList(models.Model):
    name = models.CharField(max_length=255, blank=True)
    genes = models.TextField(blank=True)
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    def __str__(self):
            return self.name
