from subprocess import run
import gzip
from datetime import datetime

from multiprocessing import Pool


# files = ['sample.vcf','sample2.vcf','sample3.vcf','sample4.vcf',]

# print(files)
file = '/storage3/1000genomes/ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf'
c_genotypes = 0
print(file)
vcf = open(file)
for line in vcf:
    if not line.startswith('#'):
        genotypes = line.strip().split('\t')[9:]
        for gen in genotypes:
            # if gen != '0|0':
            c_genotypes += 1
            #     list_genotypes.add(gen)
            #     if gen not in list_genotypes:
            #         list_genotypes.append(gen)
    # return(list_genotypes)
print(c_genotypes)
