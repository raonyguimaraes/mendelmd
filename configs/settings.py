import os

# MAIN SETTINGS

snpEff_memory = "4G"
snpsift_memory = "4G"
snpsift_merge_memory = "4G"
vep_cores = 4
vcf_annotator_cores = 4
dbnsfp_cores = 4
vcfanno_cores = 4
func_pred_cores = 2

# LIBS SETTINGS
BASE_DIR = os.path.dirname(__file__)
libs_dir = os.path.join(BASE_DIR, 'libs')
data_dir = os.path.join(BASE_DIR, 'data')

# ##LIBS

# htslib (tabix)
htslib_version = '1.9'
htslib_file = f'htslib-{htslib_version}.tar.bz2'
htslib_source = f'https://github.com/samtools/htslib/releases/download/{htslib_version}/{htslib_file}'
htslib_dir = f'{libs_dir}/htslib/htslib-{htslib_version}'

vcfanno_dir = f'{libs_dir}/vcfanno/'

# vcftools
vcftools_version = '0.1.16'
vcftools_file = f'vcftools-{vcftools_version}.tar.gz'
vcftools_source = f'https://github.com/vcftools/vcftools/releases/download/' \
                  f'v{vcftools_version}/vcftools-{vcftools_version}.tar.gz'

# validation
vcftools_dir = f"{libs_dir}/vcftools/vcftools-{vcftools_version}/src/cpp"
vcftools_dir_perl = f"{libs_dir}/vcftools/vcftools-{vcftools_version}/src/perl"
vcf_validator_dir = f"{libs_dir}/vcf-validator"

# snpeff
snpeff_database = 'GRCh37.75'  # this is the last build from GRCh37
# snpeff_version = 'snpEff_latest_core'
snpeff_version = 'snpEff_v4_3t_core'  # need to test version 4.3
snpeff_source = f'http://sourceforge.net/projects/snpeff/files/{snpeff_version}.zip'

snpeff_dir = os.path.join(libs_dir, 'snpeff', 'snpEff')
snpeff_data_dir = os.path.join(data_dir, 'snpeff_data')

# vep
vep_release = '95.1'
vep_source = f'https://github.com/Ensembl/ensembl-vep/archive/release/{vep_release}.zip'
vep_cache_dir = os.path.join(data_dir, 'vep_data')
vep_dir = f'{libs_dir}/vep/src/ensembl-vep/'

# gemini
gemini_file = 'gemini_install.py'
gemini_source = f'https://github.com/arq5x/gemini/raw/master/gemini/scripts/{gemini_file}'

# ##Datasets

# Decipher
hi_predictions_file = 'HI_Predictions_Version3.bed.gz'
hi_predictions_source = f'https://decipher.sanger.ac.uk/files/downloads/{hi_predictions_file}'
hi_predictions = f'{data_dir}/decipher/{hi_predictions_file}'

population_cnv_file = 'population_cnv.txt.gz'
population_cnv_source = f'https://decipher.sanger.ac.uk/files/downloads/{population_cnv_file}'

ddg2p_file = 'DDG2P.csv.gz'
ddg2p_source = f'http://www.ebi.ac.uk/gene2phenotype/downloads/{ddg2p_file}'

# ensembl #HGMD PUBLIC
vep_major_release = '95'
ensembl_phenotype_file = 'homo_sapiens_phenotype_associated.vcf.gz'
ensembl_phenotype_source = f'ftp://ftp.ensembl.org/pub/grch37/release-{vep_major_release}/' \
                           f'variation/vcf/homo_sapiens/{ensembl_phenotype_file}'

ensembl_clinically_file = 'homo_sapiens_clinically_associated.vcf.gz'
ensembl_clinically_source = f'ftp://ftp.ensembl.org/pub/grch37/release-{vep_major_release}/' \
                            f'variation/vcf/homo_sapiens/{ensembl_clinically_file}'


# 1000genomes
genomes1k_vcf = 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf'
genomes1k_file = f'{genomes1k_vcf}.gz'
genomes1k_source = f'ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/{genomes1k_file}'

# dbsnp
dbsnp_file = 'All_20180423.vcf.gz'
dbsnp_source = f'ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/{dbsnp_file}'
dbsnp = f'{data_dir}/dbsnp/{dbsnp_file}'

clinvar_file = 'clinvar.vcf.gz'
clinvar_source = f'ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/{clinvar_file}'

# ESP
esp_basename = 'ESP6500SI-V2-SSA137.GRCh38-liftover'
esp_file = f'{esp_basename}.snps_indels.vcf.tar.gz'
esp_source = f'http://evs.gs.washington.edu/evs_bulk_data/{esp_file}'
esp_final_file = 'esp6500si.vcf.gz'

# dbnsfp
dbnsfp_version = '3.5a'
dbnsfp_file = f'dbNSFP{dbnsfp_version}.txt.gz'
dbnsfp_link = f'ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbNSFPv{dbnsfp_version}.zip'
dbnsfp = f'{data_dir}/dbnsfp/dbNSFP{dbnsfp_version}.txt.gz'

# dbscsnv
dbscsnv_version = '1.1'
dbscsnv_file = f'dbscSNV{dbscsnv_version}.txt.gz'
dbscsnv_source = f'ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbscSNV{dbscsnv_version}.zip'
dbscsnv = f'{data_dir}/dbnsfp/dbscSNV{dbscsnv_version}.txt.gz'

data_file = "pynnotator-data.latest.tar"
data_source = f"https://mendelmd.org/{data_file}"

libs_file = "pynnotator-libs.latest.tar.gz"
libs_source = f"https://mendelmd.org/{libs_file}"
