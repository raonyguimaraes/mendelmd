from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Integer, Float, Boolean
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection(hosts=['es01:9200'], timeout=60)


class VariantIndex(DocType):
    individual = Integer()
    
    index = Text()
    pos_index = Text()

    # First save all 9 VCF columns
    chr = Text()
    pos = Text()
    variant_id = Text()
    ref = Text()
    alt = Text()
    qual = Float()
    filter = Text()
    info = Text()
    format = Text

    genotype_col = Text()
    genotype = Text()

    # metrics from genotype_info DP field
    read_depth = Integer()

    gene = Text()
    mutation_type = Text()
    vartype = Text()

    # Annotation From 1000genomes
    genomes1k_maf = Float()
    dbsnp_maf = Float()
    esp_maf = Float()

    # dbsnp
    dbsnp_build = Integer()

    # VEP
    sift = Float()
    sift_pred = Text()

    polyphen2 = Float()
    polyphen2_pred = Text()

    condel = Float()
    condel_pred = Text()

    dann = Float()
    cadd = Float()

    # hi_index
    hi_index_str = Text()
    hi_index = Float()
    hi_index_perc = Float()

    # OMIM
    is_at_omim = Boolean()

    # HGMD
    is_at_hgmd = Boolean()
    hgmd_entries = Text()

    # snpeff annotation
    snpeff_effect = Text()
    snpeff_impact = Text()
    snpeff_func_class = Text()
    snpeff_codon_change = Text()
    snpeff_aa_change = Text()
    snpeff_gene_name = Text()
    snpeff_biotype = Text()
    snpeff_gene_coding = Text()
    snpeff_transcript_id = Text()
    snpeff_exon_rank = Text()

    # vep annotation
    vep_allele = Text()
    vep_gene = Text()
    vep_feature = Text()
    vep_feature_type = Text()
    vep_consequence = Text()
    vep_cdna_position = Text()
    vep_cds_position = Text()
    vep_protein_position = Text()
    vep_amino_acids = Text()
    vep_codons = Text()
    vep_existing_variation = Text()
    vep_distance = Text()
    vep_strand = Text()
    vep_symbol = Text()
    vep_symbol_source = Text()
    vep_sift = Text()
    vep_polyphen = Text()
    vep_condel = Text()

    # new annotations
    ensembl_clin_HGMD = Boolean()
    clinvar_CLNSRC = Text()
    # ensembl_phen.CLIN_pathogenic
    # ensembl_phen.CLIN_likely_pathogenic
    # ensembl_clin.CLIN_pathogenic

    # DBNFSP
    SIFT_score = Text()
    SIFT_converted_rankscore = Text()
    Uniprot_acc_Polyphen2 = Text()
    Uniprot_id_Polyphen2 = Text()
    Uniprot_aapos_Polyphen2 = Text()
    Polyphen2_HDIV_score = Text()
    Polyphen2_HDIV_rankscore = Text()
    Polyphen2_HDIV_pred = Text()
    Polyphen2_HVAR_score = Text()
    Polyphen2_HVAR_rankscore = Text()
    Polyphen2_HVAR_pred = Text()
    LRT_score = Text()
    LRT_converted_rankscore = Text()
    LRT_pred = Text()
    LRT_Omega = Text()
    MutationTaster_score = Text()
    MutationTaster_converted_rankscore = Text()
    MutationTaster_pred = Text()
    MutationTaster_model = Text()
    MutationTaster_AAE = Text()
    MutationAssessor_UniprotID = Text()
    MutationAssessor_variant = Text()
    MutationAssessor_score = Text()
    MutationAssessor_rankscore = Text()
    MutationAssessor_pred = Text()
    FATHMM_score = Text()
    FATHMM_converted_rankscore = Text()
    FATHMM_pred = Text()
    PROVEAN_score = Text()
    PROVEAN_converted_rankscore = Text()
    PROVEAN_pred = Text()
    Transcript_id_VEST3 = Text()
    Transcript_var_VEST3 = Text()
    VEST3_score = Text()
    VEST3_rankscore = Text()
    MetaSVM_score = Text()
    MetaSVM_rankscore = Text()
    MetaSVM_pred = Text()
    MetaLR_score = Text()
    MetaLR_rankscore = Text()
    MetaLR_pred = Text()
    Reliability_index = Text()
    CADD_raw = Text()
    CADD_raw_rankscore = Text()
    CADD_phred = Text()
    DANN_score = Text()
    DANN_rankscore = Text()
    fathmm_MKL_coding_score = Text()
    fathmm_MKL_coding_rankscore = Text()
    fathmm_MKL_coding_pred = Text()
    fathmm_MKL_coding_group = Text()
    Eigen_raw = Text()
    Eigen_phred = Text()
    Eigen_raw_rankscore = Text()
    Eigen_PC_raw = Text()
    Eigen_PC_raw_rankscore = Text()
    GenoCanyon_score = Text()
    GenoCanyon_score_rankscore = Text()
    integrated_fitCons_score = Text()
    integrated_fitCons_rankscore = Text()
    integrated_confidence_value = Text()
    GM12878_fitCons_score = Text()
    GM12878_fitCons_rankscore = Text()
    GM12878_confidence_value = Text()
    H1_hESC_fitCons_score = Text()
    H1_hESC_fitCons_rankscore = Text()
    H1_hESC_confidence_value = Text()
    HUVEC_fitCons_score = Text()
    HUVEC_fitCons_rankscore = Text()
    HUVEC_confidence_value = Text()
    GERP_NR = Text()
    GERP_RS = Text()
    GERP_RS_rankscore = Text()
    phyloP100way_vertebrate = Text()
    phyloP100way_vertebrate_rankscore = Text()
    phyloP20way_mammalian = Text()
    phyloP20way_mammalian_rankscore = Text()
    phastCons100way_vertebrate = Text()
    phastCons100way_vertebrate_rankscore = Text()
    phastCons20way_mammalian = Text()
    phastCons20way_mammalian_rankscore = Text()
    SiPhy_29way_pi = Text()
    SiPhy_29way_logOdds = Text()
    SiPhy_29way_logOdds_rankscore = Text()
    clinvar_rs = Text()
    clinvar_clnsig = Text()
    clinvar_trait = Text()
    clinvar_golden_stars = Text()
    mcap_score = Float()
    mcap_rankscore = Float()
    mcap_pred = Text()
    revel_score = Text()

    class Meta:
        index = 'variant-index'


def bulk_indexing():
    VariantIndex.init('variant-indexing')
    es = Elasticsearch(hosts=[{'host': 'es01', 'port': 9200}], timeout=60)
    bulk(client=es, actions=(b.indexing() for b in models.Variant.objects.all().iterator()))
