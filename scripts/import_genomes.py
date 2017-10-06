import sys, os, django
sys.path.append("/home/raony/dev/mendelmd") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mendelmd.settings")
django.setup()
from variants.models import Variant

# import psycopg2
# conn = psycopg2.connect("dbname='mendelmd' user='postgres' host='localhost' password='postgres'")

# from cyvcf2 import VCF

vcf = '/home/raony/dev/mendelmd/data/genomes/ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf'
#open vcf
vcffile = open(vcf)

# sqlcommand = """
#     COPY variants_variant ("chr", "pos")
#         FROM '/home/raony/dev/mendelmd/data/genomes/positions.tsv'
#     DELIMITER E'\t';"""
# cur = conn.cursor()    
# f = open('/home/raony/dev/mendelmd/data/genomes/positions.tsv')
# cur.copy_from(f, 'variants_variant', columns=('chr', 'pos'), sep="\t")
# conn.commit()
# conn.close()

variants_list = []

for variant in vcffile:
    if not variant.startswith('#'):
        # if len(variants_list) == 5000:
        #     Variant.objects.bulk_create(variants_list)
        #     variants = []
        variant = variant.split('\t')
        variant_obj = Variant()
        variant_obj.chr = variant[0]
        variant_obj.pos = variant[1]
        # variant_obj.save()
        variants_list.append(variant_obj)
Variant.objects.bulk_create(variants_list)

        # Variant
        #  MyModel.objects.create(name=row['NAME'], number=row['NUMBER'])


    # pass
    # print(line)
    # die()
    # print(variant.CHROM, variant.start, variant.end, variant.ID, \
				# variant.FILTER, variant.QUAL)
    # die()
    # index = '{}_{}'.format(variant.CHROM, variant.start)
    # print(index)