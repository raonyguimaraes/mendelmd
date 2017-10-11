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
vcfs = ['1000.sample.vcf']#chr21.sample.vcf

# import argparse

t_genotypes = 0
new_genotypes = []
individuals = {}
individualgenotypes = []

class GenomeImporter():
    
    def __init__(self, *args, **kwargs):
        self.c_genotypes = 0
        self.vcfs = vcfs
        self.variants = []

    # def check_file():
        # command = ''
        # command = 'vcf_validator'
        # run(command, shell=True)

    def main(self):
        # self.check_file():
        self.parse_vcf()

    def parse_genotypes(self,index, genotypes):
        print(index)
        for i, genotype in enumerate(genotypes):
            # print(genotype),
            individualvariant = IndividualVariant()
            # individualvariant.variant = self.variants[index]
            individualvariant.individual = samples[i]
            individualvariant.save()
            # individualvariants.append(individualvariant)
            self.c_genotypes+=1

    def parse_vcf(self):
        
        c_genotypes = self.c_genotypes

        start = time.time()

        for vcf in vcfs:
            
            print(vcf)
            vcffile = open('../data/genomes/%s' % (vcf))
            #Variant.objects.delete()
            start = time.time()
            index_list = Variant.objects.values_list('index', flat=True)
            # self.variants = index_list
            individuals_list = Individual.objects.values_list('name', flat=True)

            print('index_list', len(index_list))

            # print(len(alleles))
            index_list = set(index_list)
            
            alleles = {}

            variants = []
            individuals_insert_list = []
            new_index_list = []

            for line in vcffile:
                if line.startswith('#'):
                    if line.startswith('#CHROM'):
                        variant = line.strip().split('\t')
                        samples = variant[9:]
                        for sample in samples:
                            #create individual model
                            if sample not in individuals_list:
                                individual = Individual()
                                individual.name = sample
                                individuals_insert_list.append(individual)
                            # individual.save()
                            # individuals[sample] = individual
                        print('Individuals', len(individuals_list))
                        individuals = Individual.objects.bulk_create(individuals_insert_list)
                        individuals = Individual.objects.filter(name__in=individuals_list)
                        
                        new_individuals = {}
                        for individual in individuals:
                            new_individuals[individual.name] = individual
                        individuals = new_individuals


                        # print('individuals', individuals)
                        print(len(individuals), 'individuals')
                else:
                    variant = line.strip().split('\t')
                    index = '%s_%s' % (variant[0], variant[1])
                    new_index_list.append(index)
                    if index not in index_list:
                        variant_obj = Variant()
                        variant_obj.chr = variant[0]
                        variant_obj.pos = variant[1]
                        variant_obj.index = index
                        # variant_obj.rsid = variant[2]
                        # variant_obj.ref = variant[3]
                        # variant_obj.alt = variant[4]
                        # variant_obj.qual = variant[5]
                        # variant_obj.filter = variant[6]
                        # variant_obj.info = variant[7]
                        # variant_obj.format = variant[8]
                        # index
                        # variant_obj.save()
                        variants.append(variant_obj)
                    # self.parse_genotypes(index,variant[9:])
            results = Variant.objects.bulk_create(variants)
            print(results)
            variants = Variant.objects.filter(index__in=new_index_list)#values_list('index', flat=True)
            print(len(variants))
            new_variants = {}
            for variant in variants:
                new_variants[variant.index] = variant
            variants = new_variants 
            #parse genotypes
            vcffile.seek(0)
            individualvariants = []
            l_genotypes = 0
            for line in vcffile:
                if not line.startswith('#'):
                    variant = line.strip().split('\t')
                    index = '%s_%s' % (variant[0], variant[1])
                    for i,genotype in enumerate(variant[9:]):
                        self.c_genotypes+=1
                        l_genotypes+=1
                        if l_genotypes == 5000:
                            
                            IndividualVariant.objects.bulk_create(individualvariants)
                            l_genotypes = 0
                            individualvariants = []

                        individualvariant = IndividualVariant()
                        individualvariant.variant = variants[index]
                        individualvariant.individual = individuals[samples[i]]
                        individualvariants.append(individualvariant)
                        # individualvariant.save()
            IndividualVariant.objects.bulk_create(individualvariants)
    # def parse_alleles():
        # ref = variant[3]
        # alt = variant[4]

        # if index not in alleles:
        #     alleles[index] = {
        #         'ref':[],
        #         'alt':[],
        #     }

        # #  = 
        # #parse alleles
        # # ref = variant=[0]
        
        # if ref not in alleles[index]['ref']:
        #     alleles[index]['ref'].append(ref)
        # if alt not in alleles[index]['alt']:
        #     alleles[index]['alt'].append(alt)

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


            # print('n alleles', len(alleles))
            # variants = {}
            # variants_objs = Variant.objects.all()

            # for variant in variants_objs:
            #     variants[variant.index] = variant

            # print(len(variants))
            
            # alleles = Allele.objects.all()
            # print('alleles', alleles)
            
            # allele_dict = {}
            # for obj in alleles:
            #     index = obj.variant.index
            #     if index not in allele_dict:
            #         allele_dict[index] = [] 
            #     allele_dict[obj.variant.index].append(obj.allele) 
            # new_alleles = []
            # for index in alleles:
            #     # print(allele)
            #     for item in alleles[index]['ref']:
            #         #check if this allele is present
            #         if item not in allele_dict[index]:
            #             allele_obj = Allele()
            #             allele_obj.variant = variant[index]
            #             allele_obj.allele_type = 'REF'
            #             allele_obj.allele = item
            #             new_alleles.append(allele_obj)

            #     for item in alleles[index]['alt']:
            #         #check if this allele is present
            #         if item not in allele_dict[index]:    
            #             allele_obj = Allele()
            #             allele_obj.variant = variant[index]
            #             allele_obj.allele_type = 'ALT'
            #             allele_obj.allele = item
            #             new_alleles.append(allele_obj)
            # print('new alleles', new_alleles)
            # Allele.objects.bulk_create(new_alleles)
            #     # allele_obj = Allele()
            #     # allele_obj.allele = 
            #     # for ite
            # # for variant in variants_objs:
            # # variants[variant.index] = variant
            # end = time.time()
            # elapsed = end - start
            # # print(c_genotypes)
            # print('inserting variants and individuals', elapsed)
            # start = time.time()

            #creating genotypes
            # Genotype.objects.bulk_create(new_genotypes)
            # genotypes = {}
            # genotype_objs = Genotype.objects.all()
            # for genotype in genotype_objs:
            #     genotypes[genotype.genotype] = genotype
            # print(genotypes)
            
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
            # print('time for inserting genotypes', elapsed)
        
        end = time.time()
        elapsed = end - start
        print('Run Time {}'.format(elapsed))
        print(self.c_genotypes)

if __name__ == "__main__":
    

    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    # args = parser.parse_args()
    #  
    gi = GenomeImporter()
    gi.main()
