from django.core.management.base import BaseCommand, CommandError

from django.db import connection
from subprocess import run
import gzip
from databases.models import Genome1kVariant, Genome1kSample, Genome1kGenotype, Genome1kSampleVariant, Genome1kVariantIndex
from datetime import datetime
from itertools import combinations
import os
        
class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Import data from 1000Genomes'

    def handle(self, *args, **options):

        # Genome1kVariant.objects.all().delete()
        # Genome1kVariantIndex.objects.all().delete()

        files = self.get_files()

        # self.add_samples(files)
        # self.add_genotypes()
        # self.add_variants(files)
        self.add_indexes(files)
        self.add_sample_genotypes(files)


    def get_files(self):

        path = '/storage3/1000genomes/ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502'
        autossomes = list(range(1,23))
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
        print('add variants')
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
                        if count == 100000:
                            print("Inserting %s " % (count2))
                            Genome1kVariant.objects.bulk_create(variants)
                            count = 0
                            variants = []
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
                        variant.qual = row[5]
                        variant.filter = row[6]
                        variant.info = row[7]
                        variant.format = row[8]
                        # variant.save()
                        variants.append(variant)
            Genome1kVariant.objects.bulk_create(variants)

    def add_indexes(self, files):

        print('add indexes')
        for file in files:
            indexes = []
            count = 0
            count2 = 0
            print(file)
            with open(file, 'rt') as f:
                for line in f:
                    if not line.startswith('#'):
                        row = line.strip().split('\t')
                        alt = row[4].split(',')
                        for item in alt:
                            count+=1
                            if count == 100000:
                                print("Inserting %s " % (count))
                                Genome1kVariantIndex.objects.bulk_create(indexes)
                                count = 0
                                indexes = []
                            index = '{}-{}-{}-{}'.format(row[0], row[1], row[3], item)
                            index_obj = Genome1kVariantIndex()
                            index_obj.index = index
                            try:
                                index_obj.variant = Genome1kVariant.objects.get(pos_index='{}-{}'.format(row[0], row[1]), ref=row[3], alt=row[4])
                            except:
                                print('duplicated index!')
                                print(row)
                            indexes.append(index_obj)
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
            print(file)
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
                        row = line.strip().split('\t')
                        genotypes = row[9:]
                        #get variant
                        index = '{}-{}'.format(row[0], row[1])
                        variant = Genome1kVariant.objects.get(pos_index=index, ref=row[3], alt=row[4])
                        for i, genotype in enumerate(genotypes):
                            if genotype != '0|0':
                                count2 += 1
                                count += 1
                                if count2 == 10000000:
                                    output.writelines('\.\n\n')
                                    output.writelines('COPY public.databases_genome1ksamplevariant (id, genotype_id, sample_id, variant_id) FROM stdin;\n')
                                    count2 = 0
                                output.writelines('{}\t{}\t{}\t{}\n'.format(count, genotypes_dict[genotype].pk, file_samples_dict[i].pk, variant.pk))
                output.writelines('\.\n')