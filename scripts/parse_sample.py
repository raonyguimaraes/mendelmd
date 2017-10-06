vcf = '/home/raony/dev/mendelmd/data/genomes/ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf'
#open vcf
vcffile = open(vcf)
for line in vcffile:
    if line.startswith('#CHROM'):
        samples = line
        break

samples = samples.split('\t')[9:]
# print(samples)
for sample in samples:
    print(sample)
