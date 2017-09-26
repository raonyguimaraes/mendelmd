from datetime import datetime
# from pgcopy import CopyManager
import psycopg2
import gzip
import re

conn = psycopg2.connect(database='mendelmd')

cols = """ "chr", "pos_1_based", "ref", "alt", "aaref", "aaalt", "rs_dbSNP150", "hg19_chr", "hg19_pos_1_based", "hg18_chr", "hg18_pos_1_based", "genename", "cds_strand", "refcodon", "codonpos", "codon_degeneracy", "Ancestral_allele", "AltaiNeandertal", "Denisova", "Ensembl_geneid", "Ensembl_transcriptid", "Ensembl_proteinid", "aapos", "SIFT_score", "SIFT_converted_rankscore", "SIFT_pred", "Uniprot_acc_Polyphen2", "Uniprot_id_Polyphen2", "Uniprot_aapos_Polyphen2", "Polyphen2_HDIV_score", "Polyphen2_HDIV_rankscore", "Polyphen2_HDIV_pred", "Polyphen2_HVAR_score", "Polyphen2_HVAR_rankscore", "Polyphen2_HVAR_pred", "LRT_score", "LRT_converted_rankscore", "LRT_pred", "LRT_Omega", "MutationTaster_score", "MutationTaster_converted_rankscore", "MutationTaster_pred", "MutationTaster_model", "MutationTaster_AAE", "MutationAssessor_UniprotID", "MutationAssessor_variant", "MutationAssessor_score", "MutationAssessor_score_rankscore", "MutationAssessor_pred", "FATHMM_score", "FATHMM_converted_rankscore", "FATHMM_pred", "PROVEAN_score", "PROVEAN_converted_rankscore", "PROVEAN_pred", "Transcript_id_VEST3", "Transcript_var_VEST3", "VEST3_score", "VEST3_rankscore", "MetaSVM_score", "MetaSVM_rankscore", "MetaSVM_pred", "MetaLR_score", "MetaLR_rankscore", "MetaLR_pred", "Reliability_index", "M_CAP_score", "M_CAP_rankscore", "M_CAP_pred", "REVEL_score", "REVEL_rankscore", "MutPred_score", "MutPred_rankscore", "MutPred_protID", "MutPred_AAchange", "MutPred_Top5features", "CADD_raw", "CADD_raw_rankscore", "CADD_phred", "DANN_score", "DANN_rankscore", "fathmm_MKL_coding_score", "fathmm_MKL_coding_rankscore", "fathmm_MKL_coding_pred", "fathmm_MKL_coding_group", "Eigen_coding_or_noncoding", "Eigen_raw", "Eigen_phred", "Eigen_PC_raw", "Eigen_PC_phred", "Eigen_PC_raw_rankscore", "GenoCanyon_score", "GenoCanyon_score_rankscore", "integrated_fitCons_score", "integrated_fitCons_score_rankscore", "integrated_confidence_value", "GM12878_fitCons_score", "GM12878_fitCons_score_rankscore", "GM12878_confidence_value", "H1_hESC_fitCons_score", "H1_hESC_fitCons_score_rankscore", "H1_hESC_confidence_value", "HUVEC_fitCons_score", "HUVEC_fitCons_score_rankscore", "HUVEC_confidence_value", "GERP_NR", "GERP_RS", "GERP_RS_rankscore", "phyloP100way_vertebrate", "phyloP100way_vertebrate_rankscore", "phyloP20way_mammalian", "phyloP20way_mammalian_rankscore", "phastCons100way_vertebrate", "phastCons100way_vertebrate_rankscore", "phastCons20way_mammalian", "phastCons20way_mammalian_rankscore", "SiPhy_29way_pi", "SiPhy_29way_logOdds", "SiPhy_29way_logOdds_rankscore", "k1000Gp3_AC", "k1000Gp3_AF", "k1000Gp3_AFR_AC", "k1000Gp3_AFR_AF", "k1000Gp3_EUR_AC", "k1000Gp3_EUR_AF", "k1000Gp3_AMR_AC", "k1000Gp3_AMR_AF", "k1000Gp3_EAS_AC", "k1000Gp3_EAS_AF", "k1000Gp3_SAS_AC", "k1000Gp3_SAS_AF", "TWINSUK_AC", "TWINSUK_AF", "ALSPAC_AC", "ALSPAC_AF", "ESP6500_AA_AC", "ESP6500_AA_AF", "ESP6500_EA_AC", "ESP6500_EA_AF", "ExAC_AC", "ExAC_AF", "ExAC_Adj_AC", "ExAC_Adj_AF", "ExAC_AFR_AC", "ExAC_AFR_AF", "ExAC_AMR_AC", "ExAC_AMR_AF", "ExAC_EAS_AC", "ExAC_EAS_AF", "ExAC_FIN_AC", "ExAC_FIN_AF", "ExAC_NFE_AC", "ExAC_NFE_AF", "ExAC_SAS_AC", "ExAC_SAS_AF", "ExAC_nonTCGA_AC", "ExAC_nonTCGA_AF", "ExAC_nonTCGA_Adj_AC", "ExAC_nonTCGA_Adj_AF", "ExAC_nonTCGA_AFR_AC", "ExAC_nonTCGA_AFR_AF", "ExAC_nonTCGA_AMR_AC", "ExAC_nonTCGA_AMR_AF", "ExAC_nonTCGA_EAS_AC", "ExAC_nonTCGA_EAS_AF", "ExAC_nonTCGA_FIN_AC", "ExAC_nonTCGA_FIN_AF", "ExAC_nonTCGA_NFE_AC", "ExAC_nonTCGA_NFE_AF", "ExAC_nonTCGA_SAS_AC", "ExAC_nonTCGA_SAS_AF", "ExAC_nonpsych_AC", "ExAC_nonpsych_AF", "ExAC_nonpsych_Adj_AC", "ExAC_nonpsych_Adj_AF", "ExAC_nonpsych_AFR_AC", "ExAC_nonpsych_AFR_AF", "ExAC_nonpsych_AMR_AC", "ExAC_nonpsych_AMR_AF", "ExAC_nonpsych_EAS_AC", "ExAC_nonpsych_EAS_AF", "ExAC_nonpsych_FIN_AC", "ExAC_nonpsych_FIN_AF", "ExAC_nonpsych_NFE_AC", "ExAC_nonpsych_NFE_AF", "ExAC_nonpsych_SAS_AC", "ExAC_nonpsych_SAS_AF", "gnomAD_exomes_AC", "gnomAD_exomes_AN", "gnomAD_exomes_AF", "gnomAD_exomes_AFR_AC", "gnomAD_exomes_AFR_AN", "gnomAD_exomes_AFR_AF", "gnomAD_exomes_AMR_AC", "gnomAD_exomes_AMR_AN", "gnomAD_exomes_AMR_AF", "gnomAD_exomes_ASJ_AC", "gnomAD_exomes_ASJ_AN", "gnomAD_exomes_ASJ_AF", "gnomAD_exomes_EAS_AC", "gnomAD_exomes_EAS_AN", "gnomAD_exomes_EAS_AF", "gnomAD_exomes_FIN_AC", "gnomAD_exomes_FIN_AN", "gnomAD_exomes_FIN_AF", "gnomAD_exomes_NFE_AC", "gnomAD_exomes_NFE_AN", "gnomAD_exomes_NFE_AF", "gnomAD_exomes_SAS_AC", "gnomAD_exomes_SAS_AN", "gnomAD_exomes_SAS_AF", "gnomAD_exomes_OTH_AC", "gnomAD_exomes_OTH_AN", "gnomAD_exomes_OTH_AF", "gnomAD_genomes_AC", "gnomAD_genomes_AN", "gnomAD_genomes_AF", "gnomAD_genomes_AFR_AC", "gnomAD_genomes_AFR_AN", "gnomAD_genomes_AFR_AF", "gnomAD_genomes_AMR_AC", "gnomAD_genomes_AMR_AN", "gnomAD_genomes_AMR_AF", "gnomAD_genomes_ASJ_AC", "gnomAD_genomes_ASJ_AN", "gnomAD_genomes_ASJ_AF", "gnomAD_genomes_EAS_AC", "gnomAD_genomes_EAS_AN", "gnomAD_genomes_EAS_AF", "gnomAD_genomes_FIN_AC", "gnomAD_genomes_FIN_AN", "gnomAD_genomes_FIN_AF", "gnomAD_genomes_NFE_AC", "gnomAD_genomes_NFE_AN", "gnomAD_genomes_NFE_AF", "gnomAD_genomes_OTH_AC", "gnomAD_genomes_OTH_AN", "gnomAD_genomes_OTH_AF", "clinvar_rs", "clinvar_clnsig", "clinvar_trait", "clinvar_golden_stars", "Interpro_domain", "GTEx_V6p_gene", "GTEx_V6p_tissue" """
cursor = conn.cursor()
# mgr = CopyManager(conn, 'databases_dbnsfp', cols)

records = []
n_obj = 0
n_total = 0

with gzip.open('/home/raony/dev/pynnotator/pynnotator/data/dbnsfp/dbNSFP3.5a.txt.gz', 'rt') as f:
    next(f)
    for line in f:
        # print(line)
        if n_obj == 5000:
            n_obj = 0
            print(n_total)

        n_obj+=1
        n_total+=1

        row = re.escape(line).strip().split('\t')
        values = "', '".join(row)
        # query =  """INSERT INTO databases_dbnsfp %s VALUES ("%s");""" % (cols, '", "'.join(row))

        # query = 'INSERT INTO ' + 'databases_dbnsfp' + ' ( ' + cols + ' ) VALUES (\'' + values + '\')' 

        # print(query)
        cursor.execute(query)
        # die()
        

        # print()
        # tuple_string = bytearray(row)
        # print(tuple_string)
        # die()
        # records.append(tuple_string)

    # mgr.copy(records)

# records = [
#         (0, now, 'Jerusalem', 72.2),
#         (1, now, 'New York', 75.6),
#         (2, now, 'Moscow', 54.3),
#     ]

