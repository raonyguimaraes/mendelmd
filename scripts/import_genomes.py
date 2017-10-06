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
            index_list = Variant.objects.values_list('index', flat=True)
            # genotypes = list(Genotype.objects.values_list('genotype', flat=True))
            # allele_list = list(Allele.objects.values_list('allele', flat=True))
            print(len(index_list))
            # print(len(alleles))
            index_list = set(index_list)
            alleles = {}
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
                    if index not in index_list:
                        variant_obj = Variant()
                        variant_obj.chr = variant[0]
                        variant_obj.pos = variant[1]
                        variant_obj.index = index
                        # variant_obj.save()
                        variants.append(variant_obj)
                    ref = variant[3]
                    alt = variant[4]

                    if index not in alleles:
                        alleles[index] = {
                            'ref':[],
                            'alt':[],
                        }
                    #  = 
                    #parse alleles
                    # ref = variant=[0]
                    if ref not in alleles[index]['ref']:
                        alleles[index]['ref'].append(ref)
                    if alt not in alleles[index]['alt']:
                        alleles[index]['alt'].append(alt)
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
            print('alleles', len(alleles))
            # Genotype.objects.bulk_create(new_genotypes)
            # genotypes = {}
            # genotype_objs = Genotype.objects.all()
            # for genotype in genotype_objs:
            #     genotypes[genotype.genotype] = genotype
            # print(genotypes)
            variants = {}
            variants_objs = Variant.objects.all()
            for variant in variants_objs:
                variants[variant.index] = variant
            alleles = Allele.objects.all()
            allele_dict = {}
            for obj in alleles:
                index = obj.variant.index
                if index not in allele_dict:
                    allele_dict[index] = [] 
                allele_dict[obj.variant.index].append(obj.allele) 
            new_alleles = []
            for index in alleles:
                # print(allele)
                for item in alleles[index]['ref']:
                    #check if this allele is present
                    if item not in allele_dict[index]:
                        allele_obj = Allele()
                        allele_obj.variant = variant[index]
                        allele_obj.allele_type = 'REF'
                        allele_obj.allele = item
                        new_alleles.append(allele_obj)

                for item in alleles[index]['alt']:
                    #check if this allele is present
                    if item not in allele_dict[index]:    
                        allele_obj = Allele()
                        allele_obj.variant = variant[index]
                        allele_obj.allele_type = 'ALT'
                        allele_obj.allele = item
                        new_alleles.append(allele_obj)
            Allele.objects.bulk_create(new_alleles)
                # allele_obj = Allele()
                # allele_obj.allele = 
                # for ite
            # for variant in variants_objs:
            # variants[variant.index] = variant
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