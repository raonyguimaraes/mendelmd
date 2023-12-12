from django import forms

class SampleGroupForm(forms.Form):
    name = forms.CharField(max_length=100)

class CreateAnalysisForm(forms.Form):
    name = forms.CharField(max_length=100)
    PIPELINES = (
               ('bwa-deepvariant-hg38', 'BWA -> Deep Variant'),
               ('bwamem2-deepvariant-hg38', 'BWA MEM 2 -> Deep Variant'),
               ('bwa-gatk4-hg38', 'BWA -> GATK4'),
               ('qc', 'FASTQ/BAM/CRAM/VCF QC'),
               ('human-genome-assembly', 'Human Genome Assembly'),
               ('ancestry-analysis', 'Ancestry Analysis'),
               ('rare-disease', 'Rare Disease Analysis'),
               ('cancer-analysis', 'Cancer Analysis'),
               )
    pipeline = forms.MultipleChoiceField(choices=PIPELINES)
    custom_pipeline_git_url = forms.CharField(max_length=600,required=False)

    GENOME_BUILDS = (
    ('GATK.GRCh38','GATK.GRCh38'),
    ('T2T-CHM13-v2.0','T2T-CHM13-v2.0'),
    ('NCBI.GRCh38','NCBI.GRCh38'),
    ('GATK.GRCh37','GATK.GRCh37'),
    ('CHM13','CHM13'),
    ('Ensembl.GRCh37','Ensembl.GRCh37'),
    )
    genome_build = forms.MultipleChoiceField(choices=GENOME_BUILDS)
    WHERE = (
    ('localhost','Localhost'),
    ('hetzner','Hetzner'),
    ('amazon','Amazon AWS'),
    ('google','Google Cloud'),
    ('azure','Azure'),
    )
    where_to_run = forms.MultipleChoiceField(choices=WHERE)