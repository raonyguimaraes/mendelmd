# Pynnotator

A Python Annotation Framework for VCF files (Exome or Genome) from Humans using multiple tools and databases.


Libraries
=========

- htslib (1.3.1)
- vcftools (0.1.14)
- snpeff (SnpEff 4.3)
- vep (version 84)

Databases
=========

- 1000Genomes (Phase 3) - ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf 
- dbSNP (including clinvar) - (human_9606_b147_GRCh37p13) 
- Exome Sequencing Project - ESP6500SI-V2-SSA137.GRCh38-liftover
- dbNFSP 3.2a (including dbscSNV 1.1) - 
- Ensembl 84 (phenotype and clinically associated variants)


Features
========
- Multithread Efficient
- Annotate a VCF file using multiple VCFs as a reference

Requirements
============

- Ubuntu 16.04 (probably also works on 14.04)
- Python 3.4+
- At least 40GB

Installation 
============

    mkvirtualenv -p /usr/bin/python3 pynnotator
    pip install cython 
    pip install pynnotator
    pynnotator install


Test
====

    pynnotator test
