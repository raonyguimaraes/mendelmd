from django.core.management.base import BaseCommand, CommandError
        
import gzip
from databases.models import dbnsfp

from django.db import connection
# print connection.queries

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Populate dbnsfp'

    def handle(self, *args, **options):

        list_obj = []
        n_obj = 0
        n_total = 0
        print('Populate dbnsfp!')
        with gzip.open('/home/raony/dev/pynnotator/pynnotator/data/dbnsfp/dbNSFP3.5a.txt.gz', 'rt') as f:
            for line in f:
                # print(line)
                if n_obj == 5000:
                    dbnsfp.objects.bulk_create(list_obj)
                    n_obj = 0
                    list_obj = []
                    print(n_total)

                n_obj+=1
                n_total+=1

                row = line.split('\t')
                db_obj = dbnsfp()
                db_obj.chr =row[0]
                db_obj.pos_1_based =row[1]
                db_obj.ref =row[2]
                db_obj.alt =row[3]
                db_obj.aaref =row[4]
                db_obj.aaalt =row[5]
                db_obj.rs_dbSNP150 = row[6]
                db_obj.hg19_chr = row[7]
                db_obj.hg19_pos_1_based = row[8]
                db_obj.hg18_chr = row[9]
                db_obj.hg18_pos_1_based = row[10]
                db_obj.genename = row[11]
                db_obj.cds_strand = row[12]
                db_obj.refcodon = row[13]
                db_obj.codonpos = row[14]
                db_obj.codon_degeneracy = row[15]
                db_obj.Ancestral_allele = row[16]
                db_obj.AltaiNeandertal = row[17]
                db_obj.Denisova = row[18]
                db_obj.Ensembl_geneid = row[19]
                db_obj.Ensembl_transcriptid = row[20]
                db_obj.Ensembl_proteinid = row[21]
                db_obj.aapos = row[22]
                db_obj.SIFT_score = row[23]
                db_obj.SIFT_converted_rankscore = row[24]
                db_obj.SIFT_pred = row[25]
                db_obj.Uniprot_acc_Polyphen2 = row[26]
                db_obj.Uniprot_id_Polyphen2 = row[27]
                db_obj.Uniprot_aapos_Polyphen2 = row[28]
                db_obj.Polyphen2_HDIV_score = row[29]
                db_obj.Polyphen2_HDIV_rankscore = row[30]
                db_obj.Polyphen2_HDIV_pred = row[31]
                db_obj.Polyphen2_HVAR_score = row[32]
                db_obj.Polyphen2_HVAR_rankscore = row[33]
                db_obj.Polyphen2_HVAR_pred = row[34]
                db_obj.LRT_score = row[35]
                db_obj.LRT_converted_rankscore = row[36]
                db_obj.LRT_pred = row[37]
                db_obj.LRT_Omega = row[38]
                db_obj.MutationTaster_score = row[39]
                db_obj.MutationTaster_converted_rankscore = row[40]
                db_obj.MutationTaster_pred = row[41]
                db_obj.MutationTaster_model = row[42]
                db_obj.MutationTaster_AAE = row[43]
                db_obj.MutationAssessor_UniprotID = row[44]
                db_obj.MutationAssessor_variant = row[45]
                db_obj.MutationAssessor_score = row[46]
                db_obj.MutationAssessor_score_rankscore = row[47]
                db_obj.MutationAssessor_pred = row[48]
                db_obj.FATHMM_score = row[49]
                db_obj.FATHMM_converted_rankscore = row[50]
                db_obj.FATHMM_pred = row[51]
                db_obj.PROVEAN_score = row[52]
                db_obj.PROVEAN_converted_rankscore = row[53]
                db_obj.PROVEAN_pred = row[54]
                db_obj.Transcript_id_VEST3 = row[55]
                db_obj.Transcript_var_VEST3 = row[56]
                db_obj.VEST3_score = row[57]
                db_obj.VEST3_rankscore = row[58]
                db_obj.MetaSVM_score = row[59]
                db_obj.MetaSVM_rankscore = row[60]
                db_obj.MetaSVM_pred = row[61]
                db_obj.MetaLR_score = row[62]
                db_obj.MetaLR_rankscore = row[63]
                db_obj.MetaLR_pred = row[64]
                db_obj.Reliability_index = row[65]
                db_obj.M_CAP_score = row[66]
                db_obj.M_CAP_rankscore = row[67]
                db_obj.M_CAP_pred = row[68]
                db_obj.REVEL_score = row[69]
                db_obj.REVEL_rankscore = row[70]
                db_obj.MutPred_score = row[71]
                db_obj.MutPred_rankscore = row[72]
                db_obj.MutPred_protID = row[73]
                db_obj.MutPred_AAchange = row[74]
                db_obj.MutPred_Top5features = row[75]
                db_obj.CADD_raw = row[76]
                db_obj.CADD_raw_rankscore = row[77]
                db_obj.CADD_phred = row[78]
                db_obj.DANN_score = row[79]
                db_obj.DANN_rankscore = row[80]
                db_obj.fathmm_MKL_coding_score = row[81]
                db_obj.fathmm_MKL_coding_rankscore = row[82]
                db_obj.fathmm_MKL_coding_pred = row[83]
                db_obj.fathmm_MKL_coding_group = row[84]
                db_obj.Eigen_coding_or_noncoding = row[85]
                db_obj.Eigen_raw = row[86]
                db_obj.Eigen_phred = row[87]
                db_obj.Eigen_PC_raw = row[88]
                db_obj.Eigen_PC_phred = row[89]
                db_obj.Eigen_PC_raw_rankscore = row[90]
                db_obj.GenoCanyon_score = row[91]
                db_obj.GenoCanyon_score_rankscore = row[92]
                db_obj.integrated_fitCons_score = row[93]
                db_obj.integrated_fitCons_score_rankscore = row[94]
                db_obj.integrated_confidence_value = row[95]
                db_obj.GM12878_fitCons_score = row[96]
                db_obj.GM12878_fitCons_score_rankscore = row[97]
                db_obj.GM12878_confidence_value = row[98]
                db_obj.H1_hESC_fitCons_score = row[99]
                db_obj.H1_hESC_fitCons_score_rankscore = row[100]
                db_obj.H1_hESC_confidence_value = row[101]
                db_obj.HUVEC_fitCons_score = row[102]
                db_obj.HUVEC_fitCons_score_rankscore = row[103]
                db_obj.HUVEC_confidence_value = row[104]
                db_obj.GERP_NR = row[105]
                db_obj.GERP_RS = row[106]
                db_obj.GERP_RS_rankscore = row[107]
                db_obj.phyloP100way_vertebrate = row[108]
                db_obj.phyloP100way_vertebrate_rankscore = row[109]
                db_obj.phyloP20way_mammalian = row[110]
                db_obj.phyloP20way_mammalian_rankscore = row[111]
                db_obj.phastCons100way_vertebrate = row[112]
                db_obj.phastCons100way_vertebrate_rankscore = row[113]
                db_obj.phastCons20way_mammalian = row[114]
                db_obj.phastCons20way_mammalian_rankscore = row[115]
                db_obj.SiPhy_29way_pi = row[116]
                db_obj.SiPhy_29way_logOdds = row[117]
                db_obj.SiPhy_29way_logOdds_rankscore = row[118]
                db_obj.k1000Gp3_AC = row[119]
                db_obj.k1000Gp3_AF = row[120]
                db_obj.k1000Gp3_AFR_AC = row[121]
                db_obj.k1000Gp3_AFR_AF = row[122]
                db_obj.k1000Gp3_EUR_AC = row[123]
                db_obj.k1000Gp3_EUR_AF = row[124]
                db_obj.k1000Gp3_AMR_AC = row[125]
                db_obj.k1000Gp3_AMR_AF = row[126]
                db_obj.k1000Gp3_EAS_AC = row[127]
                db_obj.k1000Gp3_EAS_AF = row[128]
                db_obj.k1000Gp3_SAS_AC = row[129]
                db_obj.k1000Gp3_SAS_AF = row[130]
                db_obj.TWINSUK_AC = row[131]
                db_obj.TWINSUK_AF = row[132]
                db_obj.ALSPAC_AC = row[133]
                db_obj.ALSPAC_AF = row[134]
                db_obj.ESP6500_AA_AC = row[135]
                db_obj.ESP6500_AA_AF = row[136]
                db_obj.ESP6500_EA_AC = row[137]
                db_obj.ESP6500_EA_AF = row[138]
                db_obj.ExAC_AC = row[139]
                db_obj.ExAC_AF = row[140]
                db_obj.ExAC_Adj_AC = row[141]
                db_obj.ExAC_Adj_AF = row[142]
                db_obj.ExAC_AFR_AC = row[143]
                db_obj.ExAC_AFR_AF = row[144]
                db_obj.ExAC_AMR_AC = row[145]
                db_obj.ExAC_AMR_AF = row[146]
                db_obj.ExAC_EAS_AC = row[147]
                db_obj.ExAC_EAS_AF = row[148]
                db_obj.ExAC_FIN_AC = row[149]
                db_obj.ExAC_FIN_AF = row[150]
                db_obj.ExAC_NFE_AC = row[151]
                db_obj.ExAC_NFE_AF = row[152]
                db_obj.ExAC_SAS_AC = row[153]
                db_obj.ExAC_SAS_AF = row[154]
                db_obj.ExAC_nonTCGA_AC = row[155]
                db_obj.ExAC_nonTCGA_AF = row[156]
                db_obj.ExAC_nonTCGA_Adj_AC = row[157]
                db_obj.ExAC_nonTCGA_Adj_AF = row[158]
                db_obj.ExAC_nonTCGA_AFR_AC = row[159]
                db_obj.ExAC_nonTCGA_AFR_AF = row[160]
                db_obj.ExAC_nonTCGA_AMR_AC = row[161]
                db_obj.ExAC_nonTCGA_AMR_AF = row[162]
                db_obj.ExAC_nonTCGA_EAS_AC = row[163]
                db_obj.ExAC_nonTCGA_EAS_AF = row[164]
                db_obj.ExAC_nonTCGA_FIN_AC = row[165]
                db_obj.ExAC_nonTCGA_FIN_AF = row[166]
                db_obj.ExAC_nonTCGA_NFE_AC = row[167]
                db_obj.ExAC_nonTCGA_NFE_AF = row[168]
                db_obj.ExAC_nonTCGA_SAS_AC = row[169]
                db_obj.ExAC_nonTCGA_SAS_AF = row[170]
                db_obj.ExAC_nonpsych_AC = row[171]
                db_obj.ExAC_nonpsych_AF = row[172]
                db_obj.ExAC_nonpsych_Adj_AC = row[173]
                db_obj.ExAC_nonpsych_Adj_AF = row[174]
                db_obj.ExAC_nonpsych_AFR_AC = row[175]
                db_obj.ExAC_nonpsych_AFR_AF = row[176]
                db_obj.ExAC_nonpsych_AMR_AC = row[177]
                db_obj.ExAC_nonpsych_AMR_AF = row[178]
                db_obj.ExAC_nonpsych_EAS_AC = row[179]
                db_obj.ExAC_nonpsych_EAS_AF = row[180]
                db_obj.ExAC_nonpsych_FIN_AC = row[181]
                db_obj.ExAC_nonpsych_FIN_AF = row[182]
                db_obj.ExAC_nonpsych_NFE_AC = row[183]
                db_obj.ExAC_nonpsych_NFE_AF = row[184]
                db_obj.ExAC_nonpsych_SAS_AC = row[185]
                db_obj.ExAC_nonpsych_SAS_AF = row[186]
                db_obj.gnomAD_exomes_AC = row[187]
                db_obj.gnomAD_exomes_AN = row[188]
                db_obj.gnomAD_exomes_AF = row[189]
                db_obj.gnomAD_exomes_AFR_AC = row[190]
                db_obj.gnomAD_exomes_AFR_AN = row[191]
                db_obj.gnomAD_exomes_AFR_AF = row[192]
                db_obj.gnomAD_exomes_AMR_AC = row[193]
                db_obj.gnomAD_exomes_AMR_AN = row[194]
                db_obj.gnomAD_exomes_AMR_AF = row[195]
                db_obj.gnomAD_exomes_ASJ_AC = row[196]
                db_obj.gnomAD_exomes_ASJ_AN = row[197]
                db_obj.gnomAD_exomes_ASJ_AF = row[198]
                db_obj.gnomAD_exomes_EAS_AC = row[199]
                db_obj.gnomAD_exomes_EAS_AN = row[200]
                db_obj.gnomAD_exomes_EAS_AF = row[201]
                db_obj.gnomAD_exomes_FIN_AC = row[202]
                db_obj.gnomAD_exomes_FIN_AN = row[203]
                db_obj.gnomAD_exomes_FIN_AF = row[204]
                db_obj.gnomAD_exomes_NFE_AC = row[205]
                db_obj.gnomAD_exomes_NFE_AN = row[206]
                db_obj.gnomAD_exomes_NFE_AF = row[207]
                db_obj.gnomAD_exomes_SAS_AC = row[208]
                db_obj.gnomAD_exomes_SAS_AN = row[209]
                db_obj.gnomAD_exomes_SAS_AF = row[210]
                db_obj.gnomAD_exomes_OTH_AC = row[211]
                db_obj.gnomAD_exomes_OTH_AN = row[212]
                db_obj.gnomAD_exomes_OTH_AF = row[213]
                db_obj.gnomAD_genomes_AC = row[214]
                db_obj.gnomAD_genomes_AN = row[215]
                db_obj.gnomAD_genomes_AF = row[216]
                db_obj.gnomAD_genomes_AFR_AC = row[217]
                db_obj.gnomAD_genomes_AFR_AN = row[218]
                db_obj.gnomAD_genomes_AFR_AF = row[219]
                db_obj.gnomAD_genomes_AMR_AC = row[220]
                db_obj.gnomAD_genomes_AMR_AN = row[221]
                db_obj.gnomAD_genomes_AMR_AF = row[222]
                db_obj.gnomAD_genomes_ASJ_AC = row[223]
                db_obj.gnomAD_genomes_ASJ_AN = row[224]
                db_obj.gnomAD_genomes_ASJ_AF = row[225]
                db_obj.gnomAD_genomes_EAS_AC = row[226]
                db_obj.gnomAD_genomes_EAS_AN = row[227]
                db_obj.gnomAD_genomes_EAS_AF = row[228]
                db_obj.gnomAD_genomes_FIN_AC = row[229]
                db_obj.gnomAD_genomes_FIN_AN = row[230]
                db_obj.gnomAD_genomes_FIN_AF = row[231]
                db_obj.gnomAD_genomes_NFE_AC = row[232]
                db_obj.gnomAD_genomes_NFE_AN = row[233]
                db_obj.gnomAD_genomes_NFE_AF = row[234]
                db_obj.gnomAD_genomes_OTH_AC = row[235]
                db_obj.gnomAD_genomes_OTH_AN = row[236]
                db_obj.gnomAD_genomes_OTH_AF = row[237]
                db_obj.clinvar_rs = row[238]
                db_obj.clinvar_clnsig = row[239]
                db_obj.clinvar_trait = row[240]
                db_obj.clinvar_golden_stars = row[241]
                db_obj.Interpro_domain = row[242]
                db_obj.GTEx_V6p_gene = row[243]
                db_obj.GTEx_V6p_tissue = row[244]


                # try:
                # db_obj.save()
                # except OperationalError:
                #     from django.db import connection
                
                # print(connection.queries[-1])
                # die()
                # print(dir(db_obj))
                # print(db_obj.query)
                # die()
                list_obj.append(db_obj)
                # db_obj.save()

                # Entry.objects.bulk_create([

            dbnsfp.objects.bulk_create(list_obj)
