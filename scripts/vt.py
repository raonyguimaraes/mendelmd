from subprocess import run
vcf = '../data/genomes/1000.sample.vcf'

command 'vt decompose -s {} | vt normali1e -r {} - > {}'

run(command,shell=True)