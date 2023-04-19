from django.core.management.base import BaseCommand, CommandError
from files.models import File,VCF
import os
from django.conf import settings
import time
from django.core.exceptions import ObjectDoesNotExist
import glob
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime
import json
from subprocess import run
import gzip

class Command(BaseCommand):
    help = 'Check Files'

    def handle(self, *args, **options):
        start_time = time.time()
        print('Check Files')
        files = File.objects.all()#.delete()
        vcfs = []
        for file in files:
            if file.name.endswith('.vcf.gz'):
                # print(file.name, file.location)
                with gzip.open(file.location, 'rt') as f:
                    #file_content = f.read()
                    build = ''
                    count_line = 0
                    count_header = 0
                    rs_pos = {}
                    for line in f:
                        if line.startswith('#'):
                            count_header +=1
                            if 'Homo_sapiens_assembly18' in line:
                                build = 'hg18'
                            if 'hg19' in line:
                                build = 'hg19'
                            if 'human_g1k_v37' in line:
                                build = 'b37'
                            if line.startswith('##reference'):
                                reference = line
                                if 'hg19' in reference:
                                    build = 'hg19'
                                if 'b37' in reference:
                                    build = 'b37'
                                if 'GRCh38' in reference:
                                    build = 'GRCh38'
                                if 'NCBI37' in reference:
                                    build = 'NCBI37'
                                if 'ftp://ftp.ensembl.org/pub/release-75/fasta/homo_sapiens/dna/' in reference:
                                    build = 'GRCh37'
                                if 'GRCh37' in reference:
                                    build = 'GRCh37'
                                if 'NCBI36' in reference:
                                    build = 'NCBI36'
                                #print(reference)
                            if line.startswith('##commandline'):
                                pass
                                #print(line)
                                if 'hg19' in line:
                                    build = 'hg19'
                                if 'b37' in line:
                                    build = 'b37'
                            if line.startswith('##contig'):
                                if 'hg19' in line:
                                    build = 'hg19'
                                if 'b37' in line:
                                    build = 'b37'
                                if '##contig=<ID=chrM,length=16571>':
                                    build = 'b37,chrM'
                            if line.startswith('#CHROM'):
                                n_samples = len(line.split('\t')[9:])

                            #print(line)
                        else:
                            count_line +=1
                            # row = line.split('\t')
                            # if len(row) > 2:
                            #     #print(row)
                            #     if row[2].startswith('rs'):
                            #         rs_pos[row[2]] = '{}:{}'.format(row[0],row[1])
                            # if count_line >=1000:
                            #     break

                    if build == '':
                        print('Could not find for ',count_header, file.location, file.name)
                    vcf = VCF(
                        file=file,
                        n_header=count_header,
                        n_variants=count_line,
                        build=build,
                        n_samples=n_samples                       
                        )
                    vcfs.append(vcf)

            # print(file.name,file.location)
            #move file for inspecting it
            #command = 'mkdir -p /projects/wasabi/{}'.format(file.id)
            #run(command,shell=True)
            #command = 'rsync {} /projects/wasabi/{}/'.format(file.location,file.id,)
            #run(command,shell=True)
            # if file.location.endwith('.vcf'):
            #     command = 'bgzip {}'.format(file.location)
        VCF.objects.bulk_create(vcfs)
        elapsed_time = time.time() - start_time
        print('Finished checking files, it took {}'.format(elapsed_time))
