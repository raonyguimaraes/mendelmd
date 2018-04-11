from subprocess import run
import gzip

path = '/storage3/1000genomes/ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502'

output = open('1kvariants.tsv', 'w')

for i in range(1,23):
    print(i)
    chr_file = '{}/ALL.chr{}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz'.format(path, i)
    with gzip.open(chr_file, 'rt') as f:
        for line in f:
            if not line.startswith('#'):
                row = line.split('\t')
                line = '\t'.join(row[0:9])
                output.writelines(line+'\n')
