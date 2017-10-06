<<<<<<< HEAD
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
=======
import time
import sys, os, django
from django.db import transaction

sys.path.append("/home/raony/dev/mendelmd") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mendelmd.settings")
django.setup()

from variants.models import Variant, IndividualVariant, Genotype, Allele
from individuals.models import Individual

vcf = '../data/genomes/ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf'
vcf = '../data/genomes/chr21.sample.vcf'
# vcfs = ['HG00096.vcf', 'HG00097.vcf']
vcfs = ['HG00096.full.vcf', 'HG00097.full.vcf']
vcfs = ['ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf']
vcfs = ['chr21.sample.vcf']


t_genotypes = 0
new_genotypes = []
individuals = {}
individualgenotypes = []

class GenomeImporter():
    
    def __init__(self, *args, **kwargs):
        self.c_genotypes = 0

    def main(self):

        c_genotypes = self.c_genotypes

        for vcf in vcfs:
            
            print(vcf)
            vcffile = open('../data/genomes/%s' % (vcf))
            #Variant.objects.delete()
            start = time.time()
            positions = Variant.objects.values_list('index', flat=True)
            # genotypes = list(Genotype.objects.values_list('genotype', flat=True))
            # allele_list = list(Allele.objects.values_list('allele', flat=True))
            print(len(positions))
            # print(len(alleles))
            new_alleles = []
            
            positions = set(positions)

            variants = []
            for line in vcffile:
                if line.startswith('#'):
                    if line.startswith('#CHROM'):
                        variant = line.strip().split('\t')
                        samples = variant[9:]
                        for sample in samples:
                            #create individual model
                            individual = Individual()
                            individual.name = sample
                            individual.save()
                            individuals[sample] = individual
                else:
                    variant = line.strip().split('\t')            
                    index = '%s_%s' % (variant[0], variant[1])
                    if index not in positions:
                        variant_obj = Variant()
                        variant_obj.chr = variant[0]
                        variant_obj.pos = variant[1]
                        variant_obj.index = index
                        # variant_obj.save()
                        variants.append(variant_obj)
                        #parse alleles
                        # ref = variant=[0]
                        # if ref not in allele_list:
                        #     allele = Allele()
                        #     allele.allele = ref
                        #     new_alleles.append(allele)
                    #genotypes
                    # for i,genotype in enumerate(variant[9:]):
                    #     # print(i)
                    #     if genotype not in genotypes:
                    #         gen_obj = Genotype(genotype=genotype)
                    #         genotypes.append(genotype)
                    #         new_genotypes.append(gen_obj)
                        # genotypes[samples[i]][index] = i
                    # obj, created = Variant.objects.get_or_create(chr=variant[0], pos=variant[1])
                    # variants = Variant.objects.filter(chr=variant[0], pos=variant[1])
                    # if len(variants) > 1:
                    #     for variant in variants:
                    #         print(variant.chr, variant.pos)
            Variant.objects.bulk_create(variants)
            # Genotype.objects.bulk_create(new_genotypes)
            # genotypes = {}
            # genotype_objs = Genotype.objects.all()
            # for genotype in genotype_objs:
            #     genotypes[genotype.genotype] = genotype
            # print(genotypes)
            # variants = {}
            variants_objs = Variant.objects.all()
            # for variant in variants_objs:
            #     variants[variant.index] = variant
            end = time.time()
            elapsed = end - start
            # print(c_genotypes)
            print('inserting variants and individuals', elapsed)
            start = time.time()
            #now insert the genotypes
            # vcffile.seek(0)
            # for line in vcffile:
            #     if not line.startswith('#'):
            #         variant = line.strip().split('\t')
            #         index = '%s_%s' % (variant[0], variant[1])
            #         for i,genotype in enumerate(variant[9:]):
            #             if genotype != '0|0':
            #                 # print(i)
            #                 c_genotypes += 1
            #                 # if c_genotypes == 1000000:
            #                 #     t_genotypes += c_genotypes
            #                 #     print(t_genotypes)
            #                 #     IndividualVariant.objects.bulk_create(individualgenotypes)
            #                 #     c_genotypes = 0
            #                 #     individualgenotypes = []
            #                 individualgenotype = IndividualVariant()
            #                 # individualgenotype.individual = individuals[samples[i]]
            #                 individualgenotype.variant = variants[index]#Variant.objects.get(index=index)
            #                 individualgenotype.genotype = genotypes[genotype]
            #                 # individualgenotypes.append(individualgenotype)
            #                 # individualgenotype.save()
            #                 # genotypes[samples[i]][index] = i
            # # IndividualVariant.objects.bulk_create(individualgenotypes)
            # end = time.time()
            # elapsed = end - start
            # print('time for inserting genotypes', elapsed)

        print(c_genotypes)

if __name__ == "__main__": 
    gi = GenomeImporter()
    gi.main()
>>>>>>> 50b83b44b896b6fe6ec61b34317df856969ea942
