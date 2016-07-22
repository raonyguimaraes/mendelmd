Annotation
==========

The annotation pipeline was developed to allow the integration of new methods and tools to the annotation process and quickly annotate your VCF files with the most possible new information available and tools.

Requirements
************

Tools
*****

- GATK
- vcftools
- Annovar - versão (Fri, 23 Aug 2013),
- VEP - versão 72
- SnpEff - versão SnpEff 3.3h (build 2013-08-20), by Pablo Cingolani

Files
*****

- HI_Score - versão vcftools_0.1.10
- dbSNP- versão 138
- 1000Genomes - versão ALL.wgs.integrated_phase1_v3.20101123
- Exome Sequencing Project - versão 6500_si

Annotation from Command Line
****************************

In order to annotate your VCF file from the command line you can use the following command:

python ../scripts/annotator.py -v sample.1000.vcf

This should run all possible annotations against your vcf files and generate at the end of the process a VCF file that was annotated with all the possible annotations from the pipeline.

In order to help you download and visualize the data we also convert this VCF file to a CSV format that can be easily opened with in your favorite spreadsheet tool (Ex. Excel, Calc and etc)

.. figure::  ../Diagrams/Annotation_Pipeline.png
   :scale: 100 %
   :align:   center

   Mendel,MD Annotation Pipeline.

Description of Methods
**********************

First of all the run the methods "vcf-validator" from vcftools make sure this it's a valid VCF file before we start annotating.Thread 
 from
After this validation we run a script called "sanitycheck" that removes the genotypes such as [0/0, ./.] from the VCF, removes "chr" from the beggining of the CHROM column and finally sort the file on this order [1...22, X, Y, MT].

After the sanitycheck is finished we can use the "Thread" module from "threading" library to parallelize multiple tasks execute each a different program and can annotate your vcf file all simultaneously.

This is useful in situations where you have good computational resources available and you want to get the results of your tasks in the fastest tiem possible.

So in this configuration we run tools such as snpeff, annovar and VEP to annotate your vcf file with each of this tools.

After all the tasks from this tools are finished we run a script called "merge" that uses VariantAnnotator from GenomeAnalysisTK in order to integrate all the results and also annotate other fields to your VCF file such as rsid from dbSNP138.

Installation of VEP
*******************

In order to install VEP you need the following commands:

::
   perl INSTALL.pl
   #Do you want to install any cache files (y/n)? y

   #The following species/files are available; which do you want (can specify multiple separated by spaces or 0 for all):
   # 28 : homo_sapiens_vep_75.tar.gz  (3,5 GB) 
   #? 28
   #This will take an enormous amount of time and you won't even be able to see the time left for the download to finish. Do some other things during this time! 

   #Do you want to install any FASTA files (y/n)? y
   ? 27  
 - downloading Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz
 The FASTA file should be automatically detected by the VEP when using --cache or --offline. If it is not, use "--fasta /home/raony/.vep/homo_sapiens/75/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa"


   perl variant_effect_predictor.pl --offline
   #testing vep installation
   sudo perl variant_effect_predictor.pl -i example.vcf --offline  

Installing snpeff

   #wget http://sourceforge.net/projects/snpeff/files/snpEff_latest_core.zip
   wget http://downloads.sourceforge.net/project/snpeff/snpEff_v3_6_core.zip
   unzip snpEff_latest_core.zip      





Annotation Sources

- Snpeff
- VEP
- SnpSift
- HI_Index


1000Genomes

dbSNP138
VCF FileS

ESP
(VCF file)

dbNSFP2.4
http://dbnsfp.houstonbioinformatics.org/dbNSFPzip/dbNSFP2.4.readme.txt
































Annovar
*******

Annotated Fields

'Func.refGene', 'Gene.refGene', 'ExonicFunc.refGene', 'AAChange.refGene', 'phastConsElements46way', 'genomicSuperDups', 'esp6500si_all', '1000g2012apr_all', 'LJB2_SIFT', 'LJB2_PolyPhen2_HDIV', 'LJB2_PP2_HDIV_Pred', 'LJB2_PolyPhen2_HVAR', 'LJB2_PolyPhen2_HVAR_Pred', 'LJB2_LRT', 'LJB2_LRT_Pred', 'LJB2_MutationTaster', 'LJB2_MutationTaster_Pred', 'LJB_MutationAssessor', 'LJB_MutationAssessor_Pred', 'LJB2_FATHMM', 'LJB2_GERP++', 'LJB2_PhyloP', 'LJB2_SiPhy', 'cosmic65', 'avsift'

Description of the fields can be found in www.openbioinformatics.org/annovar/

Func_refGene
Gene_refGene
ExonicFunc_refGene
AAChange_refGene
phastConsElements46way
genomicSuperDups
esp6500si_all
1000g2012apr_all
LJB2_SIFT
LJB2_PolyPhen2_HDIV
LJB2_PP2_HDIV_Pred
LJB2_PolyPhen2_HVAR
LJB2_PolyPhen2_HVAR_Pred
LJB2_LRT
LJB2_LRT_Pred
LJB2_MutationTaster
LJB2_MutationTaster_Pred
LJB_MutationAssessor
LJB_MutationAssessor_Pred
LJB2_FATHMM
LJB2_GERP++
LJB2_PhyloP
LJB2_SiPhy
cosmic65
avsift

record.annovar.func_refgene
record.annovar.gene_refgene
record.annovar.exonicfunc_refgene
record.annovar.aachange_refgene
record.annovar.phastconselements46way
record.annovar.genomicsuperdups
record.annovar.esp6500si_all
record.annovar.1000g2012apr_all
record.annovar.ljb2_sift
record.annovar.ljb2_polyphen2_hdiv
record.annovar.ljb2_pp2_hdiv_pred
record.annovar.ljb2_polyphen2_hvar
record.annovar.ljb2_polyphen2_hvar_pred
record.annovar.ljb2_lrt
record.annovar.ljb2_lrt_pred
record.annovar.ljb2_mutationtaster
record.annovar.ljb2_mutationtaster_pred
record.annovar.ljb_mutationassessor
record.annovar.ljb_mutationassessor_pred
record.annovar.ljb2_fathmm
record.annovar.ljb2_gerp++
record.annovar.ljb2_phylop
record.annovar.ljb2_siphy
record.annovar.cosmic65
record.annovar.avsift

Sources: http://www.openbioinformatics.org/annovar/annovar_gene.html

func_refgene classes:
splicing
UTR5
ncRNA_exonic
intergenic
intronic
UTR3
exonic
upstream
ncRNA_intronic