from django.db import models

# Create your models here.
class VariSNP(models.Model):
    """
    Description: 

    benchmark database for neutral variations from dbSNP


    """
    dbsnp_id = models.CharField(max_length=255)
    # heterozygosity
    # heterozygosity_standard_error
    # creation_date
    # creation_build
    # update_date
    # update_build
    # observed_alleles
    # asn_from
    # asn_to
    # reference_allele
    # orientation
    # minor_allele_frequency
    # minor_allele
    # sample_size
    # validation
    # hgvs_names
    # allele_origin
    # clinical_significance
    # functional_class
    # ncbi_gi
    # ncbi_accession
    # gene_symbol
    # refseq_start_description
    # coding_dna_description
    # protein_description
    # coding_reference
    # protein_reference
    # predicted_RNA_variation
    # DNA_annotation
    # RNA_annotation
    # protein_annotation    