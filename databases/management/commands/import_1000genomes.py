from django.core.management.base import BaseCommand, CommandError

from django.db import connection
from subprocess import run
import gzip
from databases.models import Genome1kVariant, Genome1kSample, Genome1kGenotype, Genome1kSampleVariant, Genome1kVariantIndex
from datetime import datetime
from itertools import combinations
        
class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Import data from 1000Genomes'

    def handle(self, *args, **options):

        # Genome1kVariant.objects.all().delete()
        # Genome1kVariantIndex.objects.all().delete()

        files = self.get_files()

        self.add_samples(files)
        self.add_genotypes()
        self.add_variants(files)
        self.add_indexes(files)
        # self.add_sample_genotypes(files)


    def get_files(self):

        path = '/storage3/1000genomes/ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502'
        autossomes = list(range(1,3))
        files = []
        # autossomes = ['22'] #for testing purposes
        print(autossomes)
        for i in autossomes:
            file = '{}/ALL.chr{}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf'.format(path, i)
            files.append(file)
            print(i)
        # extra chrs
        chrs = ['ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf','ALL.chrY.phase3_integrated_v2a.20130502.genotypes.vcf','ALL.chrMT.phase3_callmom-v0_4.20130502.genotypes.vcf']
        for chr in chrs:
            file = '{}/{}'.format(path, chr)
            files.append(file)

        return(files)

    def add_samples(self, files):
        
        # # add samples
        samples = self.get_samples(files)
        print(len(samples))
        # print(samples)
        sample_list = []
        for sample_name in samples:
            sample = Genome1kSample()
            sample.name = sample_name
            sample_list.append(sample)

        Genome1kSample.objects.bulk_create(sample_list)

    def add_genotypes(self):

        # #add genotypes
        # genotypes = self.get_genotypes(import_files)
        geno_list = []
        genotypes = ['.', '0', '0|0', '0|1', '0|10', '0|11', '0|12', '0|2', '0|3', '0|4', '0|5', '0|6', '0|7', '0|8', '0|9', '1', '10|0', '10|1', '10|10', '10|11', '10|12', '10|2', '10|3', '10|4', '10|5', '10|6', '10|7', '10|8', '10|9', '11|0', '12|0', '1|0', '1|1', '1|10', '1|2', '1|3', '1|4', '1|5', '1|6', '1|7', '1|8', '1|9', '2', '2|0', '2|1', '2|10', '2|2', '2|3', '2|4', '2|5', '2|6', '2|7', '2|8', '3', '3|0', '3|1', '3|10', '3|2', '3|3', '3|4', '3|5', '3|6', '3|7', '3|8', '4', '4|0', '4|1', '4|10', '4|11', '4|2', '4|3', '4|4', '4|5', '4|6', '4|7', '4|8', '5', '5|0', '5|1', '5|10', '5|2', '5|3', '5|4', '5|5', '5|6', '5|7', '5|8', '5|9', '6', '6|0', '6|1', '6|10', '6|11', '6|2', '6|3', '6|4', '6|5', '6|6', '6|7', '6|8', '6|9', '7', '7|0', '7|1', '7|10', '7|2', '7|3', '7|4', '7|5', '7|6', '7|7', '7|8', '7|9', '8', '8|0', '8|1', '8|2', '8|3', '8|4', '8|5', '8|6', '8|7', '8|8', '8|9', '9', '9|0', '9|10', '9|3', '9|4', '9|5', '9|6', '9|8', '9|9']
        for gen in genotypes:
            gen_obj = Genome1kGenotype()
            gen_obj.genotype = gen
            # gen_obj.save()
            geno_list.append(gen_obj)
        Genome1kGenotype.objects.bulk_create(geno_list)

    def add_variants(self, files):

        #add variants
        ## start import variants
        for file in files:

            variants = []
            count = 0
            count2 = 0

            print(file)
            with open(file, 'rt') as f:
                # file_content = f.read()
                for line in f:
                    if not line.startswith('#'):
                        # print(line)
                        count += 1
                        count2 += 1
                        #bulk insert variants objects
                        # if count == 1000000:
                        #     print("Inserting %s " % (count2))
                        #     Genome1kVariant.objects.bulk_create(variants)
                        #     count = 0
                        #     variants = []
                        row = line.strip().split('\t')
                        # print(row)
                        variant = Genome1kVariant()
                        pos_index = '{}-{}'.format(row[0], row[1])
                        variant.pos_index = pos_index
                        variant.chrom = row[0]
                        variant.pos = row[1]
                        variant.rsid = row[2]
                        variant.ref = row[3]
                        variant.alt = row[4]
                        # variant.qual = row[5]
                        # variant.filter = row[6]
                        # variant.info = row[7]
                        # variant.format = row[8]
                        # variant.save()
                        variants.append(variant)
            Genome1kVariant.objects.bulk_create(variants)

        #now finally add genotypes to samples
        # self.add_sample_genotypes(import_files)
        # with connection.cursor() as cursor:
                # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
                # cursor.execute("""copy databases_dbnfsp ("chr","pos_1_based","ref","alt","aaref","aaalt","rs_dbSNP150","hg19_chr","hg19_pos_1_based","hg18_chr","hg18_pos_1_based","genename","cds_strand","refcodon","codonpos","codon_degeneracy","Ancestral_allele","AltaiNeandertal","Denisova","Ensembl_geneid","Ensembl_transcriptid","Ensembl_proteinid","aapos","SIFT_score","SIFT_converted_rankscore","SIFT_pred","Uniprot_acc_Polyphen2","Uniprot_id_Polyphen2","Uniprot_aapos_Polyphen2","Polyphen2_HDIV_score","Polyphen2_HDIV_rankscore","Polyphen2_HDIV_pred","Polyphen2_HVAR_score","Polyphen2_HVAR_rankscore","Polyphen2_HVAR_pred","LRT_score","LRT_converted_rankscore","LRT_pred","LRT_Omega","MutationTaster_score","MutationTaster_converted_rankscore","MutationTaster_pred","MutationTaster_model","MutationTaster_AAE","MutationAssessor_UniprotID","MutationAssessor_variant","MutationAssessor_score","MutationAssessor_score_rankscore","MutationAssessor_pred","FATHMM_score","FATHMM_converted_rankscore","FATHMM_pred","PROVEAN_score","PROVEAN_converted_rankscore","PROVEAN_pred","Transcript_id_VEST3","Transcript_var_VEST3","VEST3_score","VEST3_rankscore","MetaSVM_score","MetaSVM_rankscore","MetaSVM_pred","MetaLR_score","MetaLR_rankscore","MetaLR_pred","Reliability_index","M_CAP_score","M_CAP_rankscore","M_CAP_pred","REVEL_score","REVEL_rankscore","MutPred_score","MutPred_rankscore","MutPred_protID","MutPred_AAchange","MutPred_Top5features","CADD_raw","CADD_raw_rankscore","CADD_phred","DANN_score","DANN_rankscore","fathmm_MKL_coding_score","fathmm_MKL_coding_rankscore","fathmm_MKL_coding_pred","fathmm_MKL_coding_group","Eigen_coding_or_noncoding","Eigen_raw","Eigen_phred","Eigen_PC_raw","Eigen_PC_phred","Eigen_PC_raw_rankscore","GenoCanyon_score","GenoCanyon_score_rankscore","integrated_fitCons_score","integrated_fitCons_score_rankscore","integrated_confidence_value","GM12878_fitCons_score","GM12878_fitCons_score_rankscore","GM12878_confidence_value","H1_hESC_fitCons_score","H1_hESC_fitCons_score_rankscore","H1_hESC_confidence_value","HUVEC_fitCons_score","HUVEC_fitCons_score_rankscore","HUVEC_confidence_value","GERP_NR","GERP_RS","GERP_RS_rankscore","phyloP100way_vertebrate","phyloP100way_vertebrate_rankscore","phyloP20way_mammalian","phyloP20way_mammalian_rankscore","phastCons100way_vertebrate","phastCons100way_vertebrate_rankscore","phastCons20way_mammalian","phastCons20way_mammalian_rankscore","SiPhy_29way_pi","SiPhy_29way_logOdds","SiPhy_29way_logOdds_rankscore","Gp3_AC_1k","Gp3_AF_1k","Gp3_AFR_AC_1k","Gp3_AFR_AF_1k","Gp3_EUR_AC_1k","Gp3_EUR_AF_1k","Gp3_AMR_AC_1k","Gp3_AMR_AF_1k","Gp3_EAS_AC_1k","Gp3_EAS_AF_1k","Gp3_SAS_AC_1k","Gp3_SAS_AF_1k","TWINSUK_AC","TWINSUK_AF","ALSPAC_AC","ALSPAC_AF","ESP6500_AA_AC","ESP6500_AA_AF","ESP6500_EA_AC","ESP6500_EA_AF","ExAC_AC","ExAC_AF","ExAC_Adj_AC","ExAC_Adj_AF","ExAC_AFR_AC","ExAC_AFR_AF","ExAC_AMR_AC","ExAC_AMR_AF","ExAC_EAS_AC","ExAC_EAS_AF","ExAC_FIN_AC","ExAC_FIN_AF","ExAC_NFE_AC","ExAC_NFE_AF","ExAC_SAS_AC","ExAC_SAS_AF","ExAC_nonTCGA_AC","ExAC_nonTCGA_AF","ExAC_nonTCGA_Adj_AC","ExAC_nonTCGA_Adj_AF","ExAC_nonTCGA_AFR_AC","ExAC_nonTCGA_AFR_AF","ExAC_nonTCGA_AMR_AC","ExAC_nonTCGA_AMR_AF","ExAC_nonTCGA_EAS_AC","ExAC_nonTCGA_EAS_AF","ExAC_nonTCGA_FIN_AC","ExAC_nonTCGA_FIN_AF","ExAC_nonTCGA_NFE_AC","ExAC_nonTCGA_NFE_AF","ExAC_nonTCGA_SAS_AC","ExAC_nonTCGA_SAS_AF","ExAC_nonpsych_AC","ExAC_nonpsych_AF","ExAC_nonpsych_Adj_AC","ExAC_nonpsych_Adj_AF","ExAC_nonpsych_AFR_AC","ExAC_nonpsych_AFR_AF","ExAC_nonpsych_AMR_AC","ExAC_nonpsych_AMR_AF","ExAC_nonpsych_EAS_AC","ExAC_nonpsych_EAS_AF","ExAC_nonpsych_FIN_AC","ExAC_nonpsych_FIN_AF","ExAC_nonpsych_NFE_AC","ExAC_nonpsych_NFE_AF","ExAC_nonpsych_SAS_AC","ExAC_nonpsych_SAS_AF","gnomAD_exomes_AC","gnomAD_exomes_AN","gnomAD_exomes_AF","gnomAD_exomes_AFR_AC","gnomAD_exomes_AFR_AN","gnomAD_exomes_AFR_AF","gnomAD_exomes_AMR_AC","gnomAD_exomes_AMR_AN","gnomAD_exomes_AMR_AF","gnomAD_exomes_ASJ_AC","gnomAD_exomes_ASJ_AN","gnomAD_exomes_ASJ_AF","gnomAD_exomes_EAS_AC","gnomAD_exomes_EAS_AN","gnomAD_exomes_EAS_AF","gnomAD_exomes_FIN_AC","gnomAD_exomes_FIN_AN","gnomAD_exomes_FIN_AF","gnomAD_exomes_NFE_AC","gnomAD_exomes_NFE_AN","gnomAD_exomes_NFE_AF","gnomAD_exomes_SAS_AC","gnomAD_exomes_SAS_AN","gnomAD_exomes_SAS_AF","gnomAD_exomes_OTH_AC","gnomAD_exomes_OTH_AN","gnomAD_exomes_OTH_AF","gnomAD_genomes_AC","gnomAD_genomes_AN","gnomAD_genomes_AF","gnomAD_genomes_AFR_AC","gnomAD_genomes_AFR_AN","gnomAD_genomes_AFR_AF","gnomAD_genomes_AMR_AC","gnomAD_genomes_AMR_AN","gnomAD_genomes_AMR_AF","gnomAD_genomes_ASJ_AC","gnomAD_genomes_ASJ_AN","gnomAD_genomes_ASJ_AF","gnomAD_genomes_EAS_AC","gnomAD_genomes_EAS_AN","gnomAD_genomes_EAS_AF","gnomAD_genomes_FIN_AC","gnomAD_genomes_FIN_AN","gnomAD_genomes_FIN_AF","gnomAD_genomes_NFE_AC","gnomAD_genomes_NFE_AN","gnomAD_genomes_NFE_AF","gnomAD_genomes_OTH_AC","gnomAD_genomes_OTH_AN","gnomAD_genomes_OTH_AF","clinvar_rs","clinvar_clnsig","clinvar_trait","clinvar_golden_stars","Interpro_domain","GTEx_V6p_gene","GTEx_V6p_tissue") from '/storage3/dev/dbnfsp/dbNSFP3.5a_variant.chr{}' delimiter E'\t' csv header;""".format(i))
            # run(command, shell=True)

    def add_indexes(self, files):

        for file in files:
            indexes = []
            # count = 0
            # count2 = 0
            # print(file)
            with open(file, 'rt') as f:
                for line in f:
                    if not line.startswith('#'):
                        row = line.strip().split('\t')
                        alt = row[4].split(',')
                        for item in alt:
                            index = '{}-{}-{}-{}'.format(row[0], row[1], row[3], item)
                            index_obj = Genome1kVariantIndex()
                            index_obj.index = index
                            index_obj.variant = Genome1kVariant.objects.get(pos_index='{}-{}'.format(row[0], row[1]), ref=row[3], alt=row[4])
                            indexes.append(index_obj)
                            # index_obj.save()
                Genome1kVariantIndex.objects.bulk_create(indexes)


    def get_samples(self, import_files):
        print('get samples', import_files)
        samples_list = []
        for file in import_files:
            with open(file, 'rt') as f:
                for line in f:
                    if line.startswith('#CHROM'):
                        samples = line.strip().split('\t')[9:]
                        break
            samples_list.extend(samples)
        samples_list = set(samples_list)
        return(samples_list)
    def get_genotypes(self, import_files):
        for file in import_files[::-1] :
            print(file)
            genotypes = set()
            start = datetime.now()
            with open(file, 'rt') as f:
                for line in f:
                    if not line.startswith('#'):
                        row = set(line.strip().split('\t')[9:])
                        for geno in row:
                            if geno not in genotypes:
                                genotypes.add(geno)
                print(len(genotypes), genotypes)
            end = datetime.now()
            time_taken = end-start
            print('time_taken', time_taken)

    def add_sample_genotypes(self, import_files):
        print('add_sample_genotypes')

        samples = Genome1kSample.objects.all()
        genotypes = Genome1kGenotype.objects.all()
        samples_dict = {}
        for sample in samples:
            samples_dict[sample.name] = sample
        genotypes_dict = {}
        for genotype in genotypes:
            genotypes_dict[genotype.genotype] = genotype

        count = 0

        for file in import_files:
            obj_list = []
            count2 = 0
            with open(file, 'rt') as f:
                basename = os.path.basename(file)
                output = open('data/1000genomes/{}.sql'.format(basename), 'w')
                output.writelines('COPY public.databases_genome1ksamplevariant (id, genotype_id, sample_id, variant_id) FROM stdin;\n')
                for line in f:
                    if line.startswith('#CHROM'):
                        file_samples = line.strip().split('\t')[9:]
                        file_samples_dict = {}
                        for i, sample in enumerate(file_samples):
                            file_samples_dict[i] = samples_dict[sample]
                    elif not line.startswith('#'):
                        
                        
                        #bulk insert variants objects
                        
                        #     obj_list = []

                        row = line.strip().split('\t')
                        genotypes = row[9:]
                        #get variant
                        index = '{}-{}'.format(row[0], row[1])
                        variant = Genome1kVariant.objects.get(pos_index=index, ref=row[3], alt=row[4])
                        for i, genotype in enumerate(genotypes):
                            if genotype != '0|0':
                            #add object
                                count2 += 1
                                count += 1
                                if count2 == 10000000:
                                    output.writelines('\.\n\n')
                                    output.writelines('COPY public.databases_genome1ksamplevariant (id, genotype_id, sample_id, variant_id) FROM stdin;\n')
                                    count2 = 0
                                output.writelines('{}\t{}\t{}\t{}\n'.format(count, genotypes_dict[genotype].pk, file_samples_dict[i].pk, variant.pk))
                                # obj = Genome1kSampleVariant()
                                # obj.sample = file_samples_dict[i]
                                # obj.variant = variant
                                # obj.genotype = genotypes_dict[genotype]
                                # obj_list.append(obj)
                output.writelines('\.\n')
            # Genome1kSampleVariant.objects.bulk_create(obj_list)