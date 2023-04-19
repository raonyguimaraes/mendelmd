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

class HGMD(models.Model):
    index = models.TextField(db_index=True)
    chrom = models.TextField(null=True, blank=True, db_index=True)
    pos = models.TextField(null=True, blank=True, db_index=True)
    rsid = models.TextField(null=True, blank=True)
    ref = models.TextField(null=True, blank=True, db_index=True)
    alt = models.TextField(null=True, blank=True, db_index=True)
    qual = models.TextField(null=True, blank=True)
    filter = models.TextField(null=True, blank=True)
    mutclass = models.TextField(null=True, blank=True)
    mut = models.TextField(null=True, blank=True)
    gene = models.TextField(null=True, blank=True)
    strand = models.TextField(null=True, blank=True)
    dna = models.TextField(null=True, blank=True)
    prot = models.TextField(null=True, blank=True)
    db = models.TextField(null=True, blank=True)
    phen = models.TextField(null=True, blank=True)


class Dbnfsp(models.Model):
    chr = models.TextField(null=True, blank=True)
    pos_1_based = models.TextField(null=True, blank=True)
    ref = models.TextField(null=True, blank=True)
    alt = models.TextField(null=True, blank=True)
    aaref = models.TextField(null=True, blank=True)
    aaalt = models.TextField(null=True, blank=True)
    rs_dbSNP150 = models.TextField(null=True, blank=True)
    hg19_chr = models.TextField(null=True, blank=True)
    hg19_pos_1_based = models.TextField(null=True, blank=True)
    hg18_chr = models.TextField(null=True, blank=True)
    hg18_pos_1_based = models.TextField(null=True, blank=True)
    genename = models.TextField(null=True, blank=True)
    cds_strand = models.TextField(null=True, blank=True)
    refcodon = models.TextField(null=True, blank=True)
    codonpos = models.TextField(null=True, blank=True)
    codon_degeneracy = models.TextField(null=True, blank=True)
    Ancestral_allele = models.TextField(null=True, blank=True)
    AltaiNeandertal = models.TextField(null=True, blank=True)
    Denisova = models.TextField(null=True, blank=True)
    Ensembl_geneid = models.TextField(null=True, blank=True)
    Ensembl_transcriptid = models.TextField(null=True, blank=True)
    Ensembl_proteinid = models.TextField(null=True, blank=True)
    aapos = models.TextField(null=True, blank=True)
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
    MutationAssessor_score_rankscore = models.TextField(null=True, blank=True)
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
    M_CAP_score = models.TextField(null=True, blank=True)
    M_CAP_rankscore = models.TextField(null=True, blank=True)
    M_CAP_pred = models.TextField(null=True, blank=True)
    REVEL_score = models.TextField(null=True, blank=True)
    REVEL_rankscore = models.TextField(null=True, blank=True)
    MutPred_score = models.TextField(null=True, blank=True)
    MutPred_rankscore = models.TextField(null=True, blank=True)
    MutPred_protID = models.TextField(null=True, blank=True)
    MutPred_AAchange = models.TextField(null=True, blank=True)
    MutPred_Top5features = models.TextField(null=True, blank=True)
    CADD_raw = models.TextField(null=True, blank=True)
    CADD_raw_rankscore = models.TextField(null=True, blank=True)
    CADD_phred = models.TextField(null=True, blank=True)
    DANN_score = models.TextField(null=True, blank=True)
    DANN_rankscore = models.TextField(null=True, blank=True)
    fathmm_MKL_coding_score = models.TextField(null=True, blank=True)
    fathmm_MKL_coding_rankscore = models.TextField(null=True, blank=True)
    fathmm_MKL_coding_pred = models.TextField(null=True, blank=True)
    fathmm_MKL_coding_group = models.TextField(null=True, blank=True)
    Eigen_coding_or_noncoding = models.TextField(null=True, blank=True)
    Eigen_raw = models.TextField(null=True, blank=True)
    Eigen_phred = models.TextField(null=True, blank=True)
    Eigen_PC_raw = models.TextField(null=True, blank=True)
    Eigen_PC_phred = models.TextField(null=True, blank=True)
    Eigen_PC_raw_rankscore = models.TextField(null=True, blank=True)
    GenoCanyon_score = models.TextField(null=True, blank=True)
    GenoCanyon_score_rankscore = models.TextField(null=True, blank=True)
    integrated_fitCons_score = models.TextField(null=True, blank=True)
    integrated_fitCons_score_rankscore = models.TextField(null=True, blank=True)
    integrated_confidence_value = models.TextField(null=True, blank=True)
    GM12878_fitCons_score = models.TextField(null=True, blank=True)
    GM12878_fitCons_score_rankscore = models.TextField(null=True, blank=True)
    GM12878_confidence_value = models.TextField(null=True, blank=True)
    H1_hESC_fitCons_score = models.TextField(null=True, blank=True)
    H1_hESC_fitCons_score_rankscore = models.TextField(null=True, blank=True)
    H1_hESC_confidence_value = models.TextField(null=True, blank=True)
    HUVEC_fitCons_score = models.TextField(null=True, blank=True)
    HUVEC_fitCons_score_rankscore = models.TextField(null=True, blank=True)
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
    Gp3_AC_1k = models.TextField(null=True, blank=True)
    Gp3_AF_1k = models.TextField(null=True, blank=True)
    Gp3_AFR_AC_1k = models.TextField(null=True, blank=True)
    Gp3_AFR_AF_1k = models.TextField(null=True, blank=True)
    Gp3_EUR_AC_1k = models.TextField(null=True, blank=True)
    Gp3_EUR_AF_1k = models.TextField(null=True, blank=True)
    Gp3_AMR_AC_1k = models.TextField(null=True, blank=True)
    Gp3_AMR_AF_1k = models.TextField(null=True, blank=True)
    Gp3_EAS_AC_1k = models.TextField(null=True, blank=True)
    Gp3_EAS_AF_1k = models.TextField(null=True, blank=True)
    Gp3_SAS_AC_1k = models.TextField(null=True, blank=True)
    Gp3_SAS_AF_1k = models.TextField(null=True, blank=True)
    TWINSUK_AC = models.TextField(null=True, blank=True)
    TWINSUK_AF = models.TextField(null=True, blank=True)
    ALSPAC_AC = models.TextField(null=True, blank=True)
    ALSPAC_AF = models.TextField(null=True, blank=True)
    ESP6500_AA_AC = models.TextField(null=True, blank=True)
    ESP6500_AA_AF = models.TextField(null=True, blank=True)
    ESP6500_EA_AC = models.TextField(null=True, blank=True)
    ESP6500_EA_AF = models.TextField(null=True, blank=True)
    ExAC_AC = models.TextField(null=True, blank=True)
    ExAC_AF = models.TextField(null=True, blank=True)
    ExAC_Adj_AC = models.TextField(null=True, blank=True)
    ExAC_Adj_AF = models.TextField(null=True, blank=True)
    ExAC_AFR_AC = models.TextField(null=True, blank=True)
    ExAC_AFR_AF = models.TextField(null=True, blank=True)
    ExAC_AMR_AC = models.TextField(null=True, blank=True)
    ExAC_AMR_AF = models.TextField(null=True, blank=True)
    ExAC_EAS_AC = models.TextField(null=True, blank=True)
    ExAC_EAS_AF = models.TextField(null=True, blank=True)
    ExAC_FIN_AC = models.TextField(null=True, blank=True)
    ExAC_FIN_AF = models.TextField(null=True, blank=True)
    ExAC_NFE_AC = models.TextField(null=True, blank=True)
    ExAC_NFE_AF = models.TextField(null=True, blank=True)
    ExAC_SAS_AC = models.TextField(null=True, blank=True)
    ExAC_SAS_AF = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_AC = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_AF = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_Adj_AC = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_Adj_AF = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_AFR_AC = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_AFR_AF = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_AMR_AC = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_AMR_AF = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_EAS_AC = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_EAS_AF = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_FIN_AC = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_FIN_AF = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_NFE_AC = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_NFE_AF = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_SAS_AC = models.TextField(null=True, blank=True)
    ExAC_nonTCGA_SAS_AF = models.TextField(null=True, blank=True)
    ExAC_nonpsych_AC = models.TextField(null=True, blank=True)
    ExAC_nonpsych_AF = models.TextField(null=True, blank=True)
    ExAC_nonpsych_Adj_AC = models.TextField(null=True, blank=True)
    ExAC_nonpsych_Adj_AF = models.TextField(null=True, blank=True)
    ExAC_nonpsych_AFR_AC = models.TextField(null=True, blank=True)
    ExAC_nonpsych_AFR_AF = models.TextField(null=True, blank=True)
    ExAC_nonpsych_AMR_AC = models.TextField(null=True, blank=True)
    ExAC_nonpsych_AMR_AF = models.TextField(null=True, blank=True)
    ExAC_nonpsych_EAS_AC = models.TextField(null=True, blank=True)
    ExAC_nonpsych_EAS_AF = models.TextField(null=True, blank=True)
    ExAC_nonpsych_FIN_AC = models.TextField(null=True, blank=True)
    ExAC_nonpsych_FIN_AF = models.TextField(null=True, blank=True)
    ExAC_nonpsych_NFE_AC = models.TextField(null=True, blank=True)
    ExAC_nonpsych_NFE_AF = models.TextField(null=True, blank=True)
    ExAC_nonpsych_SAS_AC = models.TextField(null=True, blank=True)
    ExAC_nonpsych_SAS_AF = models.TextField(null=True, blank=True)
    gnomAD_exomes_AC = models.TextField(null=True, blank=True)
    gnomAD_exomes_AN = models.TextField(null=True, blank=True)
    gnomAD_exomes_AF = models.TextField(null=True, blank=True)
    gnomAD_exomes_AFR_AC = models.TextField(null=True, blank=True)
    gnomAD_exomes_AFR_AN = models.TextField(null=True, blank=True)
    gnomAD_exomes_AFR_AF = models.TextField(null=True, blank=True)
    gnomAD_exomes_AMR_AC = models.TextField(null=True, blank=True)
    gnomAD_exomes_AMR_AN = models.TextField(null=True, blank=True)
    gnomAD_exomes_AMR_AF = models.TextField(null=True, blank=True)
    gnomAD_exomes_ASJ_AC = models.TextField(null=True, blank=True)
    gnomAD_exomes_ASJ_AN = models.TextField(null=True, blank=True)
    gnomAD_exomes_ASJ_AF = models.TextField(null=True, blank=True)
    gnomAD_exomes_EAS_AC = models.TextField(null=True, blank=True)
    gnomAD_exomes_EAS_AN = models.TextField(null=True, blank=True)
    gnomAD_exomes_EAS_AF = models.TextField(null=True, blank=True)
    gnomAD_exomes_FIN_AC = models.TextField(null=True, blank=True)
    gnomAD_exomes_FIN_AN = models.TextField(null=True, blank=True)
    gnomAD_exomes_FIN_AF = models.TextField(null=True, blank=True)
    gnomAD_exomes_NFE_AC = models.TextField(null=True, blank=True)
    gnomAD_exomes_NFE_AN = models.TextField(null=True, blank=True)
    gnomAD_exomes_NFE_AF = models.TextField(null=True, blank=True)
    gnomAD_exomes_SAS_AC = models.TextField(null=True, blank=True)
    gnomAD_exomes_SAS_AN = models.TextField(null=True, blank=True)
    gnomAD_exomes_SAS_AF = models.TextField(null=True, blank=True)
    gnomAD_exomes_OTH_AC = models.TextField(null=True, blank=True)
    gnomAD_exomes_OTH_AN = models.TextField(null=True, blank=True)
    gnomAD_exomes_OTH_AF = models.TextField(null=True, blank=True)
    gnomAD_genomes_AC = models.TextField(null=True, blank=True)
    gnomAD_genomes_AN = models.TextField(null=True, blank=True)
    gnomAD_genomes_AF = models.TextField(null=True, blank=True)
    gnomAD_genomes_AFR_AC = models.TextField(null=True, blank=True)
    gnomAD_genomes_AFR_AN = models.TextField(null=True, blank=True)
    gnomAD_genomes_AFR_AF = models.TextField(null=True, blank=True)
    gnomAD_genomes_AMR_AC = models.TextField(null=True, blank=True)
    gnomAD_genomes_AMR_AN = models.TextField(null=True, blank=True)
    gnomAD_genomes_AMR_AF = models.TextField(null=True, blank=True)
    gnomAD_genomes_ASJ_AC = models.TextField(null=True, blank=True)
    gnomAD_genomes_ASJ_AN = models.TextField(null=True, blank=True)
    gnomAD_genomes_ASJ_AF = models.TextField(null=True, blank=True)
    gnomAD_genomes_EAS_AC = models.TextField(null=True, blank=True)
    gnomAD_genomes_EAS_AN = models.TextField(null=True, blank=True)
    gnomAD_genomes_EAS_AF = models.TextField(null=True, blank=True)
    gnomAD_genomes_FIN_AC = models.TextField(null=True, blank=True)
    gnomAD_genomes_FIN_AN = models.TextField(null=True, blank=True)
    gnomAD_genomes_FIN_AF = models.TextField(null=True, blank=True)
    gnomAD_genomes_NFE_AC = models.TextField(null=True, blank=True)
    gnomAD_genomes_NFE_AN = models.TextField(null=True, blank=True)
    gnomAD_genomes_NFE_AF = models.TextField(null=True, blank=True)
    gnomAD_genomes_OTH_AC = models.TextField(null=True, blank=True)
    gnomAD_genomes_OTH_AN = models.TextField(null=True, blank=True)
    gnomAD_genomes_OTH_AF = models.TextField(null=True, blank=True)
    clinvar_rs = models.TextField(null=True, blank=True)
    clinvar_clnsig = models.TextField(null=True, blank=True)
    clinvar_trait = models.TextField(null=True, blank=True)
    clinvar_golden_stars = models.TextField(null=True, blank=True)
    Interpro_domain = models.TextField(null=True, blank=True)
    GTEx_V6p_gene = models.TextField(null=True, blank=True)
    GTEx_V6p_tissue = models.TextField(null=True, blank=True)


class Genome1kVariant(models.Model):
    pos_index = models.TextField(db_index=True)#ex. 1-326754756
    chrom = models.TextField(null=True, blank=True, db_index=True)
    pos = models.TextField(null=True, blank=True, db_index=True)
    rsid = models.TextField(null=True, blank=True)
    ref = models.TextField(null=True, blank=True, db_index=True)
    alt = models.TextField(null=True, blank=True, db_index=True)
    qual = models.TextField(null=True, blank=True)
    filter = models.TextField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    format = models.TextField(null=True, blank=True)

class Genome1kVariantIndex(models.Model):
    index = models.TextField()#ex. 1-2387623-G-T REF ALT for each REF and ALT
    variant = models.ForeignKey(Genome1kVariant, on_delete=models.CASCADE)

class Genome1kSample(models.Model):
    name = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class Genome1kGenotype(models.Model):
    genotype = models.TextField(null=True, blank=True)

class Genome1kSampleVariant(models.Model):
    sample = models.ForeignKey(Genome1kSample, on_delete=models.CASCADE)
    variant = models.ForeignKey(Genome1kVariant, on_delete=models.CASCADE)
    genotype = models.ForeignKey(Genome1kGenotype, on_delete=models.CASCADE)
    # class Meta:
    #    managed = False
    #or add a fake primary key
    #https://groups.google.com/forum/#!topic/django-users/nRPURDAlgH0

