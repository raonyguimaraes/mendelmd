from django.db import models
from individuals.models import Individual

class Variant(models.Model):

    individual = models.ForeignKey(Individual)
    
    index = models.TextField()#ex. 1-2387623-G-T
    pos_index = models.TextField()#ex. 1-326754756

    #First save all 9 VCF columns
    chr = models.TextField(verbose_name="Chr")
    pos = models.IntegerField()
    variant_id = models.TextField(verbose_name="ID")    
    ref = models.TextField(null=True, blank=True)
    alt = models.TextField(null=True, blank=True)
    qual = models.FloatField()
    filter = models.TextField()
    info = models.TextField(null=True, blank=True)
    format = models.TextField(null=True, blank=True)
    
    genotype_col = models.TextField(null=True, blank=True)
    genotype = models.TextField()

    #metrics from genotype_info DP field
    read_depth = models.IntegerField()

    gene = models.TextField(null=True, blank=True)
    mutation_type = models.TextField(null=True)    
    vartype = models.TextField(null=True)

    #Annotation From 1000genomes 
    genomes1k_maf = models.FloatField(null=True, blank=True, verbose_name="1000 Genomes Frequency")
    dbsnp_maf = models.FloatField(null=True, blank=True, verbose_name="dbSNP Frequency")
    esp_maf = models.FloatField(null=True, blank=True, verbose_name="ESP6500 Frequency")
    
    #dbsnp
    # dbsnp_pm = models.TextField(null=True, blank=True)
    # dbsnp_clnsig = models.TextField(null=True, blank=True)
    dbsnp_build = models.IntegerField(null=True)
    
    #VEP
    sift = models.FloatField(null=True, blank=True)
    sift_pred = models.TextField(null=True, blank=True)

    polyphen2 = models.FloatField(null=True, blank=True)
    polyphen2_pred = models.TextField(null=True, blank=True)

    condel = models.FloatField(null=True, blank=True)
    condel_pred = models.TextField(null=True, blank=True)

    dann = models.FloatField(null=True, blank=True)

    cadd = models.FloatField(null=True, blank=True)

    rf_score = models.FloatField(null=True, blank=True)
    ada_score = models.FloatField(null=True, blank=True)

    #hi_index
    # hi_index_str = models.TextField(null=True, blank=True)
    # hi_index = models.FloatField(null=True, blank=True)
    # hi_index_perc = models.FloatField(null=True, blank=True)

    #OMIM
    is_at_omim = models.BooleanField(default=False)

    #HGMD
    is_at_hgmd = models.BooleanField(default=False)
    hgmd_entries = models.TextField(null=True, blank=True)

    #snpeff annotation
    snpeff_effect = models.TextField(null=True, blank=True)
    snpeff_impact = models.TextField(null=True, blank=True)
    snpeff_func_class = models.TextField(null=True, blank=True)
    snpeff_codon_change = models.TextField(null=True, blank=True)
    snpeff_aa_change = models.TextField(null=True, blank=True)
    # snpeff_aa_len = models.TextField(null=True, blank=True)
    snpeff_gene_name = models.TextField(null=True, blank=True)
    snpeff_biotype = models.TextField(null=True, blank=True)
    snpeff_gene_coding = models.TextField(null=True, blank=True)
    snpeff_transcript_id = models.TextField(null=True, blank=True)
    snpeff_exon_rank = models.TextField(null=True, blank=True)
    # snpeff_genotype_number = models.TextField(null=True, blank=True)

    #vep annotation
    vep_allele = models.TextField(null=True, blank=True)
    vep_gene = models.TextField(null=True, blank=True)
    vep_feature = models.TextField(null=True, blank=True)
    vep_feature_type = models.TextField(null=True, blank=True)
    vep_consequence = models.TextField(null=True, blank=True)
    vep_cdna_position = models.TextField(null=True, blank=True)
    vep_cds_position = models.TextField(null=True, blank=True)
    vep_protein_position = models.TextField(null=True, blank=True)
    vep_amino_acids = models.TextField(null=True, blank=True)
    vep_codons = models.TextField(null=True, blank=True)
    vep_existing_variation = models.TextField(null=True, blank=True)
    vep_distance = models.TextField(null=True, blank=True)
    vep_strand = models.TextField(null=True, blank=True)
    vep_symbol = models.TextField(null=True, blank=True)
    vep_symbol_source = models.TextField(null=True, blank=True)
    vep_sift = models.TextField(null=True, blank=True)
    vep_polyphen = models.TextField(null=True, blank=True)
    vep_condel = models.TextField(null=True, blank=True)

    #new annotations
    ensembl_clin_HGMD = models.BooleanField(default=False)
    ensembl_clin_HGMD = models.BooleanField(default=False)
    clinvar_CLNSRC = models.TextField(null=True, blank=True)
    # ensembl_phen.CLIN_pathogenic
    #ensembl_phen.CLIN_likely_pathogenic
    # ensembl_clin.CLIN_pathogenic

    #DBNFSP
    SIFT_score = models.TextField(null=True, blank=True)
    SIFT_converted_rankscore = models.TextField(null=True, blank=True)
    SIFT_pred = models.TextField(null=True, blank=True)
    Uniprot_acc_Polyphen2 = models.TextField(null=True, blank=True)
    Uniprot_id_Polyphen2 = models.TextField(null=True, blank=True)
    Uniprot_aapos_Polyphen2 = models.TextField(null=True, blank=True)
    Polyphen2_HDIV_score = models.TextField(null=True, blank=True)
    Polyphen2_HDIV_rankscore = models.TextField(null=True, blank=True)
    Polyphen2_HDIV_pred = models.TextField(null=True, blank=True)
    Polyphen2_HVAR_score = models.TextField(null=True, blank=True)
    Polyphen2_HVAR_rankscore = models.TextField(null=True, blank=True)
    Polyphen2_HVAR_pred = models.TextField(null=True, blank=True)
    LRT_score = models.TextField(null=True, blank=True)
    LRT_converted_rankscore = models.TextField(null=True, blank=True)
    LRT_pred = models.TextField(null=True, blank=True)
    LRT_Omega = models.TextField(null=True, blank=True)
    MutationTaster_score = models.TextField(null=True, blank=True)
    MutationTaster_converted_rankscore = models.TextField(null=True, blank=True)
    MutationTaster_pred = models.TextField(null=True, blank=True)
    MutationTaster_model = models.TextField(null=True, blank=True)
    MutationTaster_AAE = models.TextField(null=True, blank=True)
    MutationAssessor_UniprotID = models.TextField(null=True, blank=True)
    MutationAssessor_variant = models.TextField(null=True, blank=True)
    MutationAssessor_score = models.TextField(null=True, blank=True)
    MutationAssessor_rankscore = models.TextField(null=True, blank=True)
    MutationAssessor_pred = models.TextField(null=True, blank=True)
    FATHMM_score = models.TextField(null=True, blank=True)
    FATHMM_converted_rankscore = models.TextField(null=True, blank=True)
    FATHMM_pred = models.TextField(null=True, blank=True)
    PROVEAN_score = models.TextField(null=True, blank=True)
    PROVEAN_converted_rankscore = models.TextField(null=True, blank=True)
    PROVEAN_pred = models.TextField(null=True, blank=True)
    Transcript_id_VEST3 = models.TextField(null=True, blank=True)
    Transcript_var_VEST3 = models.TextField(null=True, blank=True)
    VEST3_score = models.TextField(null=True, blank=True)
    VEST3_rankscore = models.TextField(null=True, blank=True)
    MetaSVM_score = models.TextField(null=True, blank=True)
    MetaSVM_rankscore = models.TextField(null=True, blank=True)
    MetaSVM_pred = models.TextField(null=True, blank=True)
    MetaLR_score = models.TextField(null=True, blank=True)
    MetaLR_rankscore = models.TextField(null=True, blank=True)
    MetaLR_pred = models.TextField(null=True, blank=True)
    Reliability_index = models.TextField(null=True, blank=True)
    CADD_raw = models.TextField(null=True, blank=True)
    CADD_raw_rankscore = models.TextField(null=True, blank=True)
    CADD_phred = models.TextField(null=True, blank=True)
    DANN_score = models.TextField(null=True, blank=True)
    DANN_rankscore = models.TextField(null=True, blank=True)
    fathmm_MKL_coding_score = models.TextField(null=True, blank=True)
    fathmm_MKL_coding_rankscore = models.TextField(null=True, blank=True)
    fathmm_MKL_coding_pred = models.TextField(null=True, blank=True)
    fathmm_MKL_coding_group = models.TextField(null=True, blank=True)
    Eigen_raw = models.TextField(null=True, blank=True)
    Eigen_phred = models.TextField(null=True, blank=True)
    Eigen_raw_rankscore = models.TextField(null=True, blank=True)
    Eigen_PC_raw = models.TextField(null=True, blank=True)
    Eigen_PC_raw_rankscore = models.TextField(null=True, blank=True)
    GenoCanyon_score = models.TextField(null=True, blank=True)
    GenoCanyon_score_rankscore = models.TextField(null=True, blank=True)
    integrated_fitCons_score = models.TextField(null=True, blank=True)
    integrated_fitCons_rankscore = models.TextField(null=True, blank=True)
    integrated_confidence_value = models.TextField(null=True, blank=True)
    GM12878_fitCons_score = models.TextField(null=True, blank=True)
    GM12878_fitCons_rankscore = models.TextField(null=True, blank=True)
    GM12878_confidence_value = models.TextField(null=True, blank=True)
    H1_hESC_fitCons_score = models.TextField(null=True, blank=True)
    H1_hESC_fitCons_rankscore = models.TextField(null=True, blank=True)
    H1_hESC_confidence_value = models.TextField(null=True, blank=True)
    HUVEC_fitCons_score = models.TextField(null=True, blank=True)
    HUVEC_fitCons_rankscore = models.TextField(null=True, blank=True)
    HUVEC_confidence_value = models.TextField(null=True, blank=True)
    GERP_NR = models.TextField(null=True, blank=True)
    GERP_RS = models.TextField(null=True, blank=True)
    GERP_RS_rankscore = models.TextField(null=True, blank=True)
    phyloP100way_vertebrate = models.TextField(null=True, blank=True)
    phyloP100way_vertebrate_rankscore = models.TextField(null=True, blank=True)
    phyloP20way_mammalian = models.TextField(null=True, blank=True)
    phyloP20way_mammalian_rankscore = models.TextField(null=True, blank=True)
    phastCons100way_vertebrate = models.TextField(null=True, blank=True)
    phastCons100way_vertebrate_rankscore = models.TextField(null=True, blank=True)
    phastCons20way_mammalian = models.TextField(null=True, blank=True)
    phastCons20way_mammalian_rankscore = models.TextField(null=True, blank=True)
    SiPhy_29way_pi = models.TextField(null=True, blank=True)
    SiPhy_29way_logOdds = models.TextField(null=True, blank=True)
    SiPhy_29way_logOdds_rankscore = models.TextField(null=True, blank=True)
    clinvar_rs = models.TextField(null=True, blank=True)
    clinvar_clnsig = models.TextField(null=True, blank=True)
    clinvar_trait = models.TextField(null=True, blank=True)
    clinvar_golden_stars = models.TextField(null=True, blank=True)


    def get_fields(self):
    	return [(field.name, field.verbose_name.title().replace('_', ' ')) for field in Variant._meta.fields]

