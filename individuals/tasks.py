# -*- coding: utf-8 -*-

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

# from celery.task import Task
# from celery.registry import tasks
from django.db import transaction
from django.core.files import File
# from celery import task

from individuals.models import *

from variants.models import *

# from mysql_bulk_insert import bulk_insert
from django.shortcuts import render, get_object_or_404
import os
import shlex
import shutil
import datetime
from django.core.mail import send_mail
# from snpedia.models import *
from diseases.models import HGMDMutation
from django.conf import settings

import zipfile
import gzip
import pickle
import tarfile
from collections import OrderedDict


import json
import vcf

from datetime import timedelta
from django.template.defaultfilters import slugify


_STANDARD_GT_HEADER = '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n'


def normalize_vcf_header(vcf_path):
    """Rewrite a non-standard FORMAT/GT declaration in place.

    Some converters (e.g. 23andMe/AncestryDNA to VCF tools) declare GT as
    Type=Integer; htslib then rejects every "0/1" call after VEP has run.
    Only the header is inspected; the body is copied unchanged.
    Returns True when the file was rewritten.
    """
    header, needs_fix = [], False
    with open(vcf_path, 'r', encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if not line.startswith('##'):
                break
            if line.startswith('##FORMAT=<ID=GT,') and 'Type=String' not in line:
                line, needs_fix = _STANDARD_GT_HEADER, True
            header.append(line)
    if not needs_fix:
        return False
    tmp = vcf_path + '.tmp'
    with open(vcf_path, 'r', encoding='utf-8', errors='replace') as src, open(tmp, 'w', encoding='utf-8') as dst:
        for line in src:
            if line.startswith('##FORMAT=<ID=GT,') and 'Type=String' not in line:
                line = _STANDARD_GT_HEADER
            elif not line.startswith('##'):
                dst.write(line)
                shutil.copyfileobj(src, dst)
                break
            dst.write(line)
    os.replace(tmp, vcf_path)
    return True


def _copy_first_vcf_from_tar(tar_path, target_path):
    """Copy the first regular *.vcf member of a .tar.gz to target_path.

    Uses extractfile() instead of tar.extract(), which honours member paths
    and links (../, absolute paths, symlinks) and could write anywhere.
    Returns True when a VCF member was found.
    """
    with tarfile.open(tar_path, "r:gz") as tar:
        for member in tar:
            if member.isfile() and member.name.endswith('.vcf'):
                with tar.extractfile(member) as source, open(target_path, 'wb') as target:
                    shutil.copyfileobj(source, target)
                return True
    return False


def _safe_stem(sample_name):
    """File-name-safe version of a VCF sample name (no paths, no shell metacharacters)."""
    import re
    stem = re.sub(r'[^A-Za-z0-9._-]', '_', str(sample_name)).lstrip('.')
    return stem or 'sample'


@shared_task()
def clean_individuals():
    print("Running periodic task!")
    individuals = Individual.objects.filter(user=None)
    for individual in individuals:
        time_difference = datetime.datetime.now()-individual.creation_date
        if time_difference.days > 0:
            #delete individuals
            os.system('rm -rf %s/genomes/public/%s' % (settings.BASE_DIR, individual_id))
            individual.delete()

@shared_task()
def VerifyVCF(individual_id):
    print('Verify VCF...')

    individual = get_object_or_404(Individual, pk=individual_id)
    print(individual.vcf_file)
    filename = str(individual.vcf_file.name.split('/')[-1])

    if individual.user:
        path  = '%s/genomes/%s/%s' % (settings.BASE_DIR, slugify(individual.user.username), individual.id)
    else:
        path  = '%s/genomes/public/%s' % (settings.BASE_DIR, individual.id)

    new_path = '/'.join(path.split('/')[:-1])
    
    print(new_path)

    orig_cwd = os.getcwd()
    os.chdir(path)
    
    print('filename', filename)

    if filename.endswith('.vcf'):
        command = 'cp %s sample.vcf' % (shlex.quote(filename))
        os.system(command)
    elif filename.endswith('.gz'):
        command = 'gunzip -c -d %s > sample.vcf' % (shlex.quote(filename))
        os.system(command)
    elif filename.endswith('.zip'):
        command = 'unzip -p %s > sample.vcf' % (shlex.quote(filename))
        os.system(command)
    elif filename.endswith('.rar'):
        command = 'unrar e %s' % (shlex.quote(filename))
        os.system(command)
        #now change filename to sample.vcf
        command = 'mv %s sample.vcf' % (shlex.quote(filename.replace('.rar', '')))
        os.system(command)


    vcf_reader = vcf.Reader(open('sample.vcf', 'r'))
    n_samples = len(vcf_reader.samples)
    print('n_samples', n_samples)

    if n_samples > 1:
        #extract individuals and create new users
        for sample in vcf_reader.samples:
            print(sample)
            command = "bcftools view -c 1 -s %s sample.vcf  > %s" % (shlex.quote(sample), shlex.quote(_safe_stem(sample) + ".vcf"))
            print(command)
            os.system(command)
        #now rename original sample
        first_sample = vcf_reader.samples[0]
        original_name = individual.name
        individual.name += ' %s' % (first_sample)
        individual.vcf_file = "%s/%s/%s.vcf" % (new_path, individual.id, _safe_stem(first_sample))
        individual.save()
        AnnotateVariants.delay(individual.id)
        #create other samples
        for sample in vcf_reader.samples[1:]:
            print(sample)
            new_individual = Individual.objects.create(user=individual.user, status='new')
            new_individual.name = original_name + ' %s' % (sample)
            output_folder = '../%s' % (new_individual.id)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                os.chmod(output_folder, 0o777)
            command = 'mv %s %s' % (shlex.quote(_safe_stem(sample) + '.vcf'), shlex.quote(output_folder))
            os.system(command)
            new_individual.vcf_file = '%s/%s/%s.vcf' % (new_path, new_individual.id, _safe_stem(sample))
            new_individual.save()
            AnnotateVariants.delay(new_individual.id)
    else:
        AnnotateVariants.delay(individual_id)

    os.chdir(orig_cwd)

    #check if VCF is multisample
    #if so extract individuals and create other individual models
    #if not send it to be annotated

def _detect_vcf_build(vcf_path):
    """Return 'hg38' or 'hg19' by scanning VCF meta-info lines; defaults to hg38."""
    try:
        with open(vcf_path, 'r') as f:
            for line in f:
                if not line.startswith('#'):
                    break
                ll = line.lower()
                if 'grch38' in ll or 'hg38' in ll:
                    return 'hg38'
                if 'grch37' in ll or 'hg19' in ll:
                    return 'hg19'
    except Exception:
        pass
    return 'hg38'


@shared_task()
def AnnotateVariants(individual_id):

    print('Annotation Started!!!')
    start = datetime.datetime.now()

    individual = get_object_or_404(Individual, pk=individual_id)

    individual.status = 'running'
    individual.save()
    

    #chdir into folder
    # print 'individual.vcf_file.name'
    # print individual.vcf_file.name
    if individual.user:
        path  = '%s/genomes/%s/%s' % (settings.BASE_DIR,  slugify(individual.user.username), individual.id)
        email = individual.user.email
    else:
        path  = '%s/genomes/public/%s' % (settings.BASE_DIR, individual.id)
        email = 'raonyguimaraes@gmail.com'
    orig_path = os.getcwd()
    #change to path for the individual folder
    os.chdir(path)
    # print(os.getcwd())

    #delete annotation folder before start annotating
    command = 'rm -rf ann_*'
    os.system(command)

    filename = str(individual.vcf_file.name.split('/')[-1])
    print(filename)
    #deal with different types of compressed files
    #ex. zip, vcf, gz, rar
    #check if user uploaded a compressed vcf
    if filename.endswith('.vcf'):
        command = 'cp %s sample.vcf' % (shlex.quote(filename))
        os.system(command)
    elif filename.endswith('.tar.gz'):
        print('targz')
        _copy_first_vcf_from_tar(filename, 'sample.vcf')
    
    if filename.endswith('.vcf.gz'):
        command = 'gunzip -c -d %s > sample.vcf' % (shlex.quote(filename))
        os.system(command)
    if filename.endswith('.zip'):
        command = 'unzip -p %s > sample.vcf' % (shlex.quote(filename))
        os.system(command)
    if filename.endswith('.rar'):
        command = 'unrar e %s' % (shlex.quote(filename))
        os.system(command)
        #now change filename to sample.vcf
        command = 'mv %s sample.vcf' % (shlex.quote(filename.replace('.rar', '')))
        os.system(command)


    #     individual.vcf_file.name = individual.vcf_file.name.replace('.zip', '.vcf')


    if os.path.exists('sample.vcf'):
        import argparse
        from pynnotator.annotator import Annotator
        build = _detect_vcf_build('sample.vcf')
        print('Detected build:', build)
        ann_args = argparse.Namespace(vcf_file=os.path.abspath('sample.vcf'), build=build)
        try:
            normalize_vcf_header('sample.vcf')
            Annotator(ann_args).run()
        except Exception as exc:
            # Without this the sample stayed "running" forever and the worker
            # kept this sample's folder as its working directory.
            print('Annotation failed for individual %s: %s' % (individual.id, exc))
            individual.status = 'failed'
            individual.annotation_time = datetime.datetime.now() - start
            individual.save(update_fields=['status', 'annotation_time'])
            os.chdir(settings.BASE_DIR)
            return
        os.chdir(path)

    #get sample name using pyvcf

    vcf_filename = os.path.splitext(os.path.basename(str(filename)))[0]

    # create a folder for the annotation if it doesn't exists,
    # or delete and create if the folder already exists

    #first check if annotation succedded
    annotation_final_file = 'ann_sample/annotation.final.vcf'

    # print('checking destination ', annotation_final_file)
    stop = datetime.datetime.now()
    elapsed = stop - start

    individual.annotation_time = elapsed

    if os.path.exists(annotation_final_file) and os.path.getsize(annotation_final_file) > 0:

        individual.status = 'annotated'
        #send email
        message = """The file %s was annotated with success!\n
It took %s to execute. \n
Now we need to insert this data to the database.
                """ % (individual.name, elapsed)
        #send_mail('[Mendel,MD] Annotation Completed!', message, 'rockbio@rockbio.io',
        #          ['raonyguimaraes@gmail.com', email], fail_silently=False)
        #delete ann folder
        command = 'rm -rf ann_*'
        # os.system(command)
        #delete sample
        command = 'rm -rf sample.vcf'
        os.system(command)

        #zip, and delete annotation folder

        command = 'zip annotation.final.vcf.zip ann_sample/annotation.final.vcf'
        os.system(command)

        individual.save()

        PopulateVariants.delay(individual.id)

        if individual.vcf_file.name.endswith(".vcf"):
            command = 'bgzip %s' % (shlex.quote(filename))
            os.system(command)
            individual.vcf_file.name = '%s.gz' % (individual.vcf_file.name)
            individual.save(update_fields=['vcf_file'])

    else:
        individual.status = 'failed'
        message = """The Individual %s failed to be annotated!\n
                It took %s to execute.
                """ % (individual.name, elapsed)
        #send_mail('[Mendel,MD] Annotation Failed!', message, 'rockbio1@gmail.com',
        ##          ['raonyguimaraes@gmail.com'], fail_silently=False)
        individual.save()

    os.chdir(settings.BASE_DIR)

def treat_float_max(float_string):
    max_value = -100
    values = float_string.split(',')
    for value in values:
        if value != '.':
            float_value = float(value)
            if float_value > max_value:
                max_value = float_value
    return max_value

def treat_float_min(float_string):
    minimum_value = 1
    values = float_string.split(',')
    for value in values:
        if value != '.':
            float_value = float(value)
            if float_value < minimum_value:
                minimum_value = float_value
    return minimum_value

def parse_vcf(line):

    """
    This function is responsible for parsing the VCF file that is generated by our annotator pipeline and
    return a dictionary with the fields to be included in the database

    Receives variant_line and return variant dict
    """

    variant = OrderedDict()
    #parse first VCF Lines
    variant_line = line.strip().split('\t')
    # print(variant_line)


    variant['chr'] = variant_line[0]

    #treat vcfs with chr on the begining of chromossome names
    if variant['chr'].startswith('chr'):
      variant['chr'] = variant['chr'].replace('chr', '')

    variant['pos'] = variant_line[1]
    variant['variant_id'] = variant_line[2]
    variant['ref'] = variant_line[3]
    variant['alt'] = variant_line[4]

    #this is form strange vcfs without qual values
    if variant_line[5] == "-1" or variant_line[5] == ".":
        variant['qual'] = 0.0
    else:
        variant['qual'] = variant_line[5]

    variant['filter'] = variant_line[6]

    variant['format'] = variant_line[-2].split(':')

    variant['genotype_col'] = variant_line[-1].split(':')

    variant['genotype'] = variant['genotype_col'][0]

    # print 'genotype', variant['genotype_col'], variant['genotype']

    if variant['genotype'] != './.':
        #fix because of isaac variant caller, there is no DP
        if 'DP' in variant['format']:
            value = variant['genotype_col'][variant['format'].index('DP')]
            if value.isdigit():
                variant['read_depth'] = int(value)
            else:
                # print('not an integer', value, variant['pos'])
                variant['read_depth'] = 0
        else:
            variant['read_depth'] = 0
    else:
        variant['read_depth'] = 0

    #annotations
    info = variant_line[7]
    string = info.split(';')

    #create a dict with all annotations at INFO field
    information = {}
    # dbnfsp_fields = []
    for element in string:
      #get all tags from line
      element = element.split('=')
      tag = element[0]
      if len(element) > 1:
        information[tag] = element[1]#.decode("utf-8", "ignore")
      else:
        information[tag] = tag
        # if element[0].startswith('dbNSFP'):
        #     dbnfsp_fields.append(element)
    if 'HET' in  information:
        variant['mutation_type'] = 'HET'
    elif 'HOM' in  information:
        variant['mutation_type'] = 'HOM'
    else:
        variant['mutation_type'] = None

    if 'VARTYPE' in  information:
        variant['vartype'] = information['VARTYPE']
    else:
        variant['vartype'] = None

    #serialize object with pickle
    variant['info'] = json.dumps(information)#.decode("utf-8", "ignore")

    # print 'information dict'
    # print information

    #parse VEP
    #Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|SYMBOL_SOURCE|HGNC_ID|SIFT|PolyPhen

    if 'CSQ' in information:
        vep = OrderedDict()
        vep_list = information['CSQ'].split('|')

        vep['Allele'] = vep_list[0]
        vep['Consequence'] = vep_list[1]
        vep['IMPACT'] = vep_list[2]
        vep['SYMBOL'] = vep_list[3]
        vep['Gene'] = vep_list[4]
        vep['Feature_type'] = vep_list[5]
        vep['Feature'] = vep_list[6]
        vep['BIOTYPE'] = vep_list[7]
        vep['EXON'] = vep_list[8]
        vep['INTRON'] = vep_list[9]
        vep['HGVSc'] = vep_list[10]
        vep['HGVSp'] = vep_list[11]

        vep['cDNA_position'] = vep_list[12]
        vep['CDS_position'] = vep_list[13]
        vep['Protein_position'] = vep_list[14]
        vep['Amino_acids'] = vep_list[15]
        vep['Codons'] = vep_list[16]
        vep['Existing_variation'] = vep_list[17]
        vep['DISTANCE'] = vep_list[18]
        vep['STRAND'] = vep_list[19]
        vep['FLAGS'] = vep_list[20]

        vep['SYMBOL_SOURCE'] = vep_list[21]
        vep['HGNC_ID'] = vep_list[22]
        vep['sift'] = vep_list[23]
        vep['polyphen2'] = vep_list[24]


        # print vep
        variant['vep'] = vep
        variant['gene'] = vep['SYMBOL']

    else:
        variant['gene'] = None

    #treat vep sift, polyphen
    csq_list = ['sift', 'polyphen2']
    for tag in csq_list:
        tag_pred = '%s_pred' % (tag)

        variant[tag]=None
        variant[tag_pred]=None

        if 'vep' in variant:
            if vep[tag] != '':
                # print('veptag', tag, vep[tag])
                value = vep[tag].split('(')
                variant[tag] = float(value[1].replace(')',''))
                variant[tag_pred] = value[0]

    #parse SNPEFF
    ##INFO=<ID=EFF,Number=.,Type=String,Description="Predicted effects for this variant.Format: 'Effect ( Effect_Impact | Functional_Class | Codon_Change | Amino_Acid_Change| Amino_Acid_length | Gene_Name | Transcript_BioType | Gene_Coding | Transcript_ID | Exon_Rank  | Genotype_Number [ | ERRORS | WARNINGS ] )' ">

    if 'EFF' in information:
        # print information['EFF']
        variant['snpeff'] = []
        effects = information['EFF'].split(',')
        # print len(effects), effects
        for ann in effects:
            snpeff = OrderedDict()

            eff_str = ann

            eff_str_list = eff_str.split('(')
            effects = eff_str_list[1].split('|')
            #EFF,Number=.,Type=String,Description="Predicted effects for this variant.Format: 'Effect ( Effect_Impact | Functional_Class | Codon_Change | Amino_Acid_Change| Amino_Acid_length | Gene_Name | Transcript_BioType | Gene_Coding | Transcript_ID | Exon_Rank  | Genotype [ | ERRORS | WARNINGS ] )' ">
            snpeff['effect'] = eff_str_list[0]
            snpeff['impact'] = effects[0]
            snpeff['func_class'] = effects[1]
            snpeff['codon_change'] = effects[2]
            snpeff['aa_change'] = effects[3]
            snpeff['aa_len'] = effects[4]
            snpeff['gene_name'] = effects[5]
            snpeff['biotype'] = effects[6]
            snpeff['gene_coding'] = effects[7]
            snpeff['transcript_id'] = effects[8]
            snpeff['exon_rank'] = effects[9]
            snpeff['genotype_number'] = effects[10].split(')')[0]
            variant['snpeff'].append(snpeff)

    float_list = ['genomes1k.AF']
    for tag in float_list:
        if tag in information:
            variant[tag] = treat_float_min(information[tag])
        else:
             variant[tag] = None

    #Special TAG FROM ESP6500
    try:
      variant['esp6500.MAF'] = float(information['esp6500.MAF'].split(',')[-1]) / 100.0
    except (KeyError):
      variant['esp6500.MAF'] = None
    #dbsnp CAF
    try:
        caf = information['dbsnp.CAF']
        caf = caf.replace('[', '').replace(']', '').split(',')
        # print 'caf', caf
        floats = []
        for x in caf:
            if x != '.':
                floats.append(float(x))
        # print sorted(floats, key=float, reverse=True)
        #get always second element from this list
        variant['dbsnp.MAF'] = floats[1]
    except (KeyError):
        variant['dbsnp.MAF'] = None

    if 'dbsnp.dbSNPBuildID' in information:
        information['dbsnp.dbSNPBuildID'] = min(information['dbsnp.dbSNPBuildID'].split(','))
        variant['dbsnp_build'] = int(information['dbsnp.dbSNPBuildID'])
    else:
        variant['dbsnp_build'] = None

    dbnfsp_fields = ['dbNSFP_SIFT_score', 'dbNSFP_SIFT_converted_rankscore', 'dbNSFP_SIFT_pred', 'dbNSFP_Uniprot_acc_Polyphen2', 'dbNSFP_Uniprot_id_Polyphen2', 'dbNSFP_Uniprot_aapos_Polyphen2', 'dbNSFP_Polyphen2_HDIV_score', 'dbNSFP_Polyphen2_HDIV_rankscore', 'dbNSFP_Polyphen2_HDIV_pred', 'dbNSFP_Polyphen2_HVAR_score', 'dbNSFP_Polyphen2_HVAR_rankscore', 'dbNSFP_Polyphen2_HVAR_pred', 'dbNSFP_LRT_score', 'dbNSFP_LRT_converted_rankscore', 'dbNSFP_LRT_pred', 'dbNSFP_LRT_Omega', 'dbNSFP_MutationTaster_score', 'dbNSFP_MutationTaster_converted_rankscore', 'dbNSFP_MutationTaster_pred', 'dbNSFP_MutationTaster_model', 'dbNSFP_MutationTaster_AAE', 'dbNSFP_MutationAssessor_UniprotID', 'dbNSFP_MutationAssessor_variant', 'dbNSFP_MutationAssessor_score', 'dbNSFP_MutationAssessor_rankscore', 'dbNSFP_MutationAssessor_pred', 'dbNSFP_FATHMM_score', 'dbNSFP_FATHMM_converted_rankscore', 'dbNSFP_FATHMM_pred', 'dbNSFP_PROVEAN_score', 'dbNSFP_PROVEAN_converted_rankscore', 'dbNSFP_PROVEAN_pred', 'dbNSFP_Transcript_id_VEST3', 'dbNSFP_Transcript_var_VEST3', 'dbNSFP_VEST3_score', 'dbNSFP_VEST3_rankscore', 'dbNSFP_MetaSVM_score', 'dbNSFP_MetaSVM_rankscore', 'dbNSFP_MetaSVM_pred', 'dbNSFP_MetaLR_score', 'dbNSFP_MetaLR_rankscore', 'dbNSFP_MetaLR_pred', 'dbNSFP_Reliability_index', 'dbNSFP_M-CAP_score', 'dbNSFP_M-CAP_rankscore', 'dbNSFP_M-CAP_pred', 'dbNSFP_REVEL_score', 'dbNSFP_REVEL_rankscore', 'dbNSFP_MutPred_score', 'dbNSFP_MutPred_rankscore', 'dbNSFP_MutPred_protID', 'dbNSFP_MutPred_AAchange', 'dbNSFP_MutPred_Top5features', 'dbNSFP_CADD_raw', 'dbNSFP_CADD_raw_rankscore', 'dbNSFP_CADD_phred', 'dbNSFP_DANN_score', 'dbNSFP_DANN_rankscore', 'dbNSFP_fathmm-MKL_coding_score', 'dbNSFP_fathmm-MKL_coding_rankscore', 'dbNSFP_fathmm-MKL_coding_pred', 'dbNSFP_fathmm-MKL_coding_group', 'dbNSFP_Eigen_coding_or_noncoding', 'dbNSFP_Eigen-raw', 'dbNSFP_Eigen-phred', 'dbNSFP_Eigen-PC-raw', 'dbNSFP_Eigen-PC-phred', 'dbNSFP_Eigen-PC-raw_rankscore', 'dbNSFP_GenoCanyon_score', 'dbNSFP_GenoCanyon_score_rankscore', 'dbNSFP_integrated_fitCons_score', 'dbNSFP_integrated_fitCons_rankscore', 'dbNSFP_integrated_confidence_value', 'dbNSFP_GM12878_fitCons_score', 'dbNSFP_GM12878_fitCons_rankscore', 'dbNSFP_GM12878_confidence_value', 'dbNSFP_H1-hESC_fitCons_score', 'dbNSFP_H1-hESC_fitCons_rankscore', 'dbNSFP_H1-hESC_confidence_value', 'dbNSFP_HUVEC_fitCons_score', 'dbNSFP_HUVEC_fitCons_rankscore', 'dbNSFP_clinvar_rs', 'dbNSFP_clinvar_clnsig', 'dbNSFP_clinvar_trait', 'dbNSFP_clinvar_golden_stars']
    dbnfsp = {}

    for field in dbnfsp_fields:
        if field in information:
            dbnfsp[field] = information[field]
        else:
            dbnfsp[field] = None
    # print(dbnfsp)

    variant['dbNSFP'] = dbnfsp

    # #cadd
    if 'dbNSFP_CADD_raw' in information:
        variant['cadd'] = treat_float_max(dbnfsp['dbNSFP_CADD_raw'])
    else:
        variant['cadd']=None

    if 'dbNSFP_M-CAP_score' in information:
        variant['mcap'] = treat_float_max(dbnfsp['dbNSFP_M-CAP_score'])
    else:
        variant['mcap']=None




    #is at OMIM
    if 'clinvar.OM' in information:
        variant['is_at_omim'] = True
    else:
        variant['is_at_omim'] = False
    #is at HGMD
    if 'HGMD' in information:
        variant['is_at_hgmd'] = True
        variant['hgmd_entries'] = information['HGMD']
    else:
        variant['is_at_hgmd'] = False
        variant['hgmd_entries'] = None

    if 'HI_PREDICTIONS' in information:
        variant['hi_index_str'] = information['HI_PREDICTIONS']
    else:
        variant['hi_index_str'] = None

    #create unique index for each chr-pos-genotype
    #genotype, ref and alt
    genotype_list = []
    genotype_list.append(variant['ref'])
    for item in variant['alt'].split(','):
        genotype_list.append(item)

    #create individual genotype list
    ind_genotype_list = []
    if len(variant['genotype']) > 1:
        if variant['genotype'][0] != '.':
            ind_genotype_list.append(genotype_list[int(variant['genotype'][0])])
        else:
            ind_genotype_list.append(genotype_list[0])
        if variant['genotype'][-1] != '.':
            ind_genotype_list.append(genotype_list[int(variant['genotype'][-1])])
        else:
            ind_genotype_list.append(genotype_list[1])

    else:
        ind_genotype_list.append(genotype_list[0])
    ind_genotype_list = sorted(ind_genotype_list)

    variant['index'] = '%s-%s-%s' % (variant['chr'], variant['pos'], "-".join(ind_genotype_list))
    variant['pos_index'] = '%s-%s' % (variant['chr'], variant['pos'])

    # print index
    # print(variant)
    return variant

def annotation_dir(individual):
    """Folder holding the individual's upload and its ann_sample/ results."""
    owner = slugify(individual.user.username) if individual.user else 'public'
    return os.path.join(settings.BASE_DIR, 'genomes', owner, str(individual.id))


def annotated_vcf_path(individual):
    """Path of the VEP-annotated VCF for an individual, or None if missing."""
    folder = annotation_dir(individual)
    for name in ('ann_sample/annotation.final.vcf', 'ann_sample/annotation.final.vcf.gz'):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return path
    return None


@shared_task()
def PopulateVariants(individual_id):
    """Load the Pynnotator 3 annotated VCF into the variants table.

    The filter, family and pathway analyses read from this table. The
    ann_sample/ folder is kept because the sample page reads its parquet file.
    """
    from individuals.populate import populate_variants

    individual = get_object_or_404(Individual, pk=individual_id)
    vcf_path = annotated_vcf_path(individual)
    if vcf_path is None:
        print('Populate skipped for %s: no annotated VCF found' % individual.id)
        return 0

    start = datetime.datetime.now()
    try:
        count = populate_variants(individual, vcf_path)
    except Exception as exc:
        # Without this the sample kept the "annotated" status from the VEP step,
        # so a genome whose variants never loaded still read as finished. That
        # is how HG002 showed as complete on 2026-06-15 while the insert had
        # aborted on an oversized btree index entry (see variants migration
        # 0003) with only 38% of its variants in the table.
        print('Populate failed for individual %s: %s' % (individual.id, exc))
        individual.status = 'failed'
        individual.insertion_time = datetime.datetime.now() - start
        individual.save(update_fields=['status', 'insertion_time'])
        raise

    individual.insertion_time = datetime.datetime.now() - start
    individual.status = 'populated'
    individual.n_lines = count
    individual.save(update_fields=['insertion_time', 'status', 'n_lines'])
    print('Individual %s populated with %s variants in %s' % (individual.id, count, individual.insertion_time))
    return count
