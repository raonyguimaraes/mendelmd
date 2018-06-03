# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from files.models import File
from .models import Task as Taskobj

import urllib.request, os

from projects.models import ProjectFile

from django.conf import settings  # noqa

from celery import Celery
app = Celery('mendelmd')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from tasks.models import Task
from workers.models import Worker
from django.db.models import Q
from workers.tasks import launch_worker, launch_workers, terminate_workers

import os
from subprocess import run, check_output
import subprocess

from individuals.tasks import parse_vcf
from individuals.models import Individual
from variants.models import Variant

from django.core.mail import send_mail

import zipfile
import gzip
import datetime
import time
import socket
import json

from urllib.parse import urlparse

from ftplib import FTP, FTP_TLS
import ftplib

from mapps.models import App
from helpers import b2_wrapper
from helpers.aws_wrapper import AWS

b2 = b2_wrapper.B2()

from multiprocessing import Lock
L = Lock()


@shared_task()
def get_file(file):
    if file.location.startswith('ftp://'):

        basename = os.path.basename(file.location)
        if not os.path.exists('input/{}'.format(basename)):
            command = 'wget -P input/ {}'.format(file.location)
            run(command, shell=True)

            command = 'md5sum input/{}'.format(basename)
            output = check_output(command, shell=True).decode('utf-8').split()[0]

            file.md5 = output
            #upload to b2
            command = 'b2 upload_file mendelmd input/{} files/{}/{}'.format(basename, file.id, basename)
            output = check_output(command, shell=True)
            
            print(output.decode('utf-8'))
            
            file.params = output.decode('utf-8')
            file.url = file.location
            file.location = 'b2://mendelmd/files/{}/{}'.format(file.id, basename)
            file.save()
    elif file.location.startswith('b2://'):

        basename = os.path.basename(file.location)

        if not os.path.exists('input/{}'.format(basename)):

            b2_location = file.location.replace('b2://mendelmd/','')
            command = 'b2 download-file-by-name mendelmd {} input/{}'.format(b2_location, basename)
            output = check_output(command, shell=True)
            print(output.decode('utf-8'))


    return(file)
    # file = File.objects.get(pk=project_file_id)
    # link = file.location

def calculate_md5(path):
    md5_dict = {}
    files = os.listdir(path)
    for file in files:
        command = 'md5sum output/{}'.format(file)
        output = check_output(command, shell=True).decode('utf-8').split()[0]
        file_md5 = output
        md5_dict[file_md5] = file
    return(md5_dict)

@shared_task()
def task_run_task(task_id):
    print('RUN TASK: ', task_id)
    log_output = ''

    task = Task.objects.get(id=task_id)
    
    task.output = ''
    
    start = datetime.datetime.now()
    manifest = task.manifest
    task.machine = socket.gethostbyname(socket.gethostname())
    task.status = 'running'
    task.started = start
    task.save()

    worker = Worker.objects.filter(ip=socket.gethostbyname(socket.gethostname())).reverse()[0]
    worker.n_tasks += 1 
    worker.status = 'running task %s' % (task.id)
    worker.started = start
    worker.save()


    task_location = '/projects/tasks/%s/' % (task.id)
    command = 'mkdir -p %s' % (task_location)
    run(command, shell=True)

    command = 'mkdir -p %s/input' % (task_location)
    run(command, shell=True)

    command = 'mkdir -p %s/output' % (task_location)
    run(command, shell=True)

    command = 'mkdir -p %s/scripts' % (task_location)
    run(command, shell=True)


    os.chdir(task_location)

    with open('manifest.json', 'w') as fp:
        json.dump(manifest, fp, sort_keys=True,indent=4)
    # file_list = []

    # for file_id in manifest['files']:        
    #     print(file_id)
    #     file = File.objects.get(pk=file_id)        
    #     file = get_file(file)
        # file_list.append(file.name)

    #start analysis
    for analysis_name in manifest['analysis_types']:
        print('analysis_name', analysis_name)
        analysis = App.objects.filter(name=analysis_name)[0]
        print(analysis)

        
        command = 'mkdir -p /projects/programs/'
        run(command, shell=True)
        os.chdir('/projects/programs/')

        basename = os.path.basename(analysis.repository)
        print('basename', basename)
        
        command = 'git clone {}'.format(analysis.source)
        run(command, shell=True)

        os.chdir(basename)

        # install
        command = 'bash scripts/install.sh'
        output = check_output(command, shell=True)

        log_output += output.decode('utf-8')
        #run
        
        os.chdir(task_location)
        command = 'python /projects/programs/{}/main.py -i {}'.format(basename, ' '.join(manifest['files']))
        print(command)
        output = run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log_output += output.stdout.decode('utf-8')


    AWS.upload(task_location+'/output', task.id)

    #upload results to b2/s3
    # md5_dict = calculate_md5('output/')
    # for hash in md5_dict:
    #     print(hash)
    #     try:
    #         file = File.objects.get(md5=hash)
    #     except:
    #         pass
    #         file = File(user=task.user)
    #         file.md5 = hash
    #         file.name = md5_dict[hash]
    #         file.save()

    #         source = 'output/{}'.format(file.name)
    #         dest = 'files/{}/{}'.format(file.id, file.name)

    #         output = b2.upload(source, dest)
            
    #         file.params = output
    #         file.location = 'b2://mendelmd/files/{}/{}'.format(file.id, file.name)
    #         file.save()    
    #         # if task.analysis:
    #         #     task.analysis_set.all()[0].files.add(file)
    #     task.files.add(file)

    # add files if needed :)

    task.status = 'done'
    stop = datetime.datetime.now()
    task.execution_time = str(stop - start)
    task.finished = stop
    task.output = log_output
    task.save()

    worker = Worker.objects.filter(ip=socket.gethostbyname(socket.gethostname())).reverse()[0]
    worker.n_tasks -= 1
    if worker.n_tasks == 0:
        worker.status = 'idle'
    worker.finished = stop
    worker.execution_time = str(stop - start)
    worker.save()
    print('Finished Task %s' % (task.name))

@app.task(queue="qc")
def run_qc(task_id):

    print('RUN QC :D')
    print('task_id', task_id)

    task = Task.objects.get(id=task_id)
    task.status = 'will be running'
    task.save()
    start = datetime.datetime.now()

    manifest = task.manifest

    task.machine = ''
    task.status = 'running'
    task.started = start
    task.save()

    # worker = Worker.objects.filter(ip=socket.gethostbyname(socket.gethostname())).reverse()[0]
    # worker.n_tasks += 1 
    # worker.status = 'running task %s' % (task.id)
    # worker.started = start
    # worker.save()

    task_location = '/projects/tasks/%s/' % (task.id)
    command = 'mkdir -p %s' % (task_location)
    run(command, shell=True)

    os.chdir(task_location)

    with open('manifest.json', 'w') as fp:
        json.dump(manifest, fp, sort_keys=True,indent=4)
    

    task.status = 'done'
    stop = datetime.datetime.now()
    task.execution_time = str(stop - start)
    task.finished = stop
    task.save()

    # worker = Worker.objects.filter(ip=socket.gethostbyname(socket.gethostname())).reverse()[0]
    
    # worker.n_tasks -= 1

    # if worker.n_tasks == 0:
    #     worker.status = 'idle'

    # worker.finished = stop
    # worker.execution_time = str(stop - start)
    # worker.save()

    print('Finished QC %s' % (task.name))


@shared_task()
def import_project_files_task(project_id):
    print('Import Files on ', project_id)

def human_size(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    """ Returns a human readable string reprentation of bytes"""
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])

@shared_task()
def compress_file(task_id):

    task = Taskobj.objects.get(pk=task_id)

    task.status = 'started'
    task.save()

    manifest = task.manifest
    file_id = manifest['file']
    print('File ID', file_id)

    file = File.objects.get(pk=file_id)
        
    if file.location.startswith('/'):

        path = '/'.join(file.location.split('/')[:-1])

        command = 'bgzip {}'.format(file.location)

        output = check_output(command, shell=True)
        
        file.last_output = output.decode('utf-8')
        file.location += '.gz'

    file.save()

    task.status = 'done'
    task.save()

@app.task(queue="annotation")
def annotate_vcf(task_id):

    start = datetime.datetime.now()

    task = Task.objects.get(id=task_id)
    task.machine = socket.gethostbyname(socket.gethostname())
    task.status = 'running'
    task.started = start
    task.save()

    print('Annotate VCF', task.id)
    individual = task.individuals.all()[0]
    print(individual.location)

    path, vcf = os.path.split(individual.location)

    task_location = '/tmp/tasks/%s/' % (task.id)
    command = 'mkdir -p %s' % (task_location)
    run(command, shell=True)
    os.chdir(task_location)

    # if not os.path.exists('%s/output/gatk'):
    # os.makedirs(directory)

    #get vcf from remote location
    worker = IWorker()
    worker.get(task.id, individual.location)
    #annotate it

    filename = vcf

    if filename.endswith('.vcf'):
        command = 'cp %s sample.vcf' % (filename)
        os.system(command)
    if filename.endswith('.gz'):
        command = 'gunzip -c -d %s > sample.vcf' % (filename)
        os.system(command)
    if filename.endswith('.zip'):
        command = 'unzip -p %s > sample.vcf' % (filename)
        os.system(command)
    if filename.endswith('.rar'):
        command = 'unrar e %s' % (filename)
        os.system(command)
        #now change filename to sample.vcf
        command = 'mv %s sample.vcf' % (filename.replace('.rar', ''))
        os.system(command)

    command = 'pynnotator -i sample.vcf'
    run(command, shell=True)

    final_file = 'ann_sample/annotation.final.vcf'
    if os.path.exists(final_file):

        command = 'zip annotation.final.vcf.zip ann_sample/annotation.final.vcf'
        run(command, shell=True)

        #send results to s3
        print('Send to S3')
        local = '/tmp/tasks/%s/annotation.final.vcf.zip' % (task.id)
        worker.put(task.id, local)
        stop = datetime.datetime.now()
        elapsed = stop - start
        individual.annotation_time = elapsed
        individual.save()
        task.status = 'annotated'
        # task.execution_time = elapsed
        task.save()

        task_location = '/tmp/tasks/%s/' % (task.id)
        command = 'rm -rf %s' % (task_location)
        run(command, shell=True)
        #add insertion task
        insert_vcf.delay(task.id)
    else:
        task.status = 'failed'
        task.retry += 1
        task.save()
        annotate_vcf.delay(task.id)

@app.task(queue="insertion")
def insert_vcf(task_id):
    task = Task.objects.get(pk=task_id)
    individual = task.individuals.all()[0]

    vcf = '/tmp/tasks/%s/annotation.final.vcf.zip' % (task.id)

    task_location = '/tmp/tasks/%s/' % (task.id)
    command = 'mkdir -p %s' % (task_location)
    run(command, shell=True)
    os.chdir(task_location)

    worker = IWorker()
    worker.get(task.id)
    task_location = '/tmp/tasks/%s/' % (task.id)
    command = 'mkdir -p %s' % (task_location)
    run(command, shell=True)
    os.chdir(task_location)

    #delete variants from individual before inserting
    Variant.objects.filter(individual=individual).delete()
    #SnpeffAnnotation.objects.filter(individual=individual).delete()
    #VEPAnnotation.objects.filter(individual=individual).delete()

    filepath = '/tmp/tasks/%s' % (task.id)

    print('Populating %s' % (individual.id))

    z = zipfile.ZipFile('%s/annotation.final.vcf.zip' % (filepath), 'r')
    data = z.open('ann_sample/annotation.final.vcf', 'r')

    start = datetime.datetime.now()
    count = 0
    variants = []
    count2 = 0

    snpeff_dict = {}
    vep_dict = {}

    for line in data:
        # print(line)
        line = line.decode("utf-8", "ignore")
        # print(line)
        # print('Hello')
        if line != '':
            if not line.startswith('#'):

                count += 1
                count2 += 1

                #bulk insert variants objects
                if count == 10000:
                    # print "Inserting %s " % (count2),
                    Variant.objects.bulk_create(variants)
                    # print ' Done!'
                    count = 0
                    variants = []

                #now parse
                variant = parse_vcf(line)
                #print(variant)
                #variant_dict['individual_id'] = individual.id
                # print 'index', variant
                # variant.snpeff.add(snpeff)
                variant_obj = Variant(
                individual=individual,
                index=variant['index'],
                pos_index=variant['pos_index'],
                chr=variant['chr'],
                pos=variant['pos'],
                variant_id=variant['variant_id'],
                ref=variant['ref'],
                alt=variant['alt'],
                qual=variant['qual'],
                filter=variant['filter'],
                info=variant['info'],
                genotype=variant['genotype'],
                genotype_col=variant['genotype_col'],
                format=variant['format'],
                read_depth=variant['read_depth'],
                gene=variant['gene'],
                mutation_type=variant['mutation_type'],
                vartype=variant['vartype'],
                genomes1k_maf=variant['genomes1k.AF'],
                dbsnp_maf=variant['dbsnp.MAF'],
                esp_maf=variant['esp6500.MAF'],
                dbsnp_build=variant['dbsnp_build'],
                sift=variant['sift'],
                sift_pred=variant['sift_pred'],
                polyphen2=variant['polyphen2'],
                polyphen2_pred=variant['polyphen2_pred'],
                # condel=variant['condel'],
                # condel_pred=variant['condel_pred'],
                cadd=variant['cadd'],
                # dann=variant['dann'],
                is_at_omim=variant['is_at_omim'],
                is_at_hgmd=variant['is_at_hgmd'],
                hgmd_entries=variant['hgmd_entries'],
                hi_index_str=variant['hi_index_str'],
                )

                # print variant['index']
                # variant_obj.save()
                #parse snpeff

                if 'snpeff' in variant:
                    #for snpeff in variant['snpeff']:
                        #snpeff = SnpeffAnnotation(
                    variant_obj.snpeff_effect=variant['snpeff'][0]['effect']
                    variant_obj.snpeff_impact=variant['snpeff'][0]['impact']
                    variant_obj.snpeff_func_class=variant['snpeff'][0]['func_class']
                    variant_obj.snpeff_codon_change=variant['snpeff'][0]['codon_change']
                    variant_obj.snpeff_aa_change=variant['snpeff'][0]['aa_change']
                    # variant_obj.snpeff_aa_len=variant['snpeff'][0]['aa_len']
                    variant_obj.snpeff_gene_name=variant['snpeff'][0]['gene_name']
                    variant_obj.snpeff_biotype=variant['snpeff'][0]['biotype']
                    variant_obj.snpeff_gene_coding=variant['snpeff'][0]['gene_coding']
                    variant_obj.snpeff_transcript_id=variant['snpeff'][0]['transcript_id']
                    variant_obj.snpeff_exon_rank=variant['snpeff'][0]['exon_rank']
                    # variant_obj.snpeff_genotype_number=variant['snpeff'][0]['genotype_number']
                    #)
                    #snpeff_dict[variant['index']] = snpeff

                #parse vep
                if 'vep' in variant:
                    #vep = VEPAnnotation(
                    variant_obj.vep_allele=variant['vep']['Allele']
                    variant_obj.vep_gene=variant['vep']['Gene']
                    variant_obj.vep_feature=variant['vep']['Feature']
                    variant_obj.vep_feature_type=variant['vep']['Feature_type']
                    variant_obj.vep_consequence=variant['vep']['Consequence']
                    variant_obj.vep_cdna_position=variant['vep']['cDNA_position']
                    variant_obj.vep_cds_position=variant['vep']['CDS_position']
                    variant_obj.vep_protein_position=variant['vep']['Protein_position']
                    variant_obj.vep_amino_acids=variant['vep']['Amino_acids']
                    variant_obj.vep_codons=variant['vep']['Codons']
                    variant_obj.vep_existing_variation=variant['vep']['Existing_variation']
                    variant_obj.vep_distance=variant['vep']['DISTANCE']
                    variant_obj.vep_strand=variant['vep']['STRAND']
                    variant_obj.vep_symbol=variant['vep']['SYMBOL']
                    variant_obj.vep_symbol_source=variant['vep']['SYMBOL_SOURCE']
                    variant_obj.vep_sift=variant['vep']['sift']
                    variant_obj.vep_polyphen=variant['vep']['polyphen2']
                    # variant_obj.vep_condel=variant['vep']['condel']
                    # variant_obj.rf_score=variant['vep']['rf_score']
                    # variant_obj.ada_score=variant['vep']['ada_score']

                    #)
                    #vep_dict[variant['index']] = vep

                if 'dbNSFP' in variant:

                    variant_obj.SIFT_score = variant['dbNSFP']['dbNSFP_SIFT_score']
                    variant_obj.SIFT_converted_rankscore = variant['dbNSFP']['dbNSFP_SIFT_converted_rankscore']
                    variant_obj.SIFT_pred = variant['dbNSFP']['dbNSFP_SIFT_pred']
                    variant_obj.Uniprot_acc_Polyphen2 = variant['dbNSFP']['dbNSFP_Uniprot_acc_Polyphen2']
                    variant_obj.Uniprot_id_Polyphen2 = variant['dbNSFP']['dbNSFP_Uniprot_id_Polyphen2']
                    variant_obj.Uniprot_aapos_Polyphen2 = variant['dbNSFP']['dbNSFP_Uniprot_aapos_Polyphen2']
                    variant_obj.Polyphen2_HDIV_score = variant['dbNSFP']['dbNSFP_Polyphen2_HDIV_score']
                    variant_obj.Polyphen2_HDIV_rankscore = variant['dbNSFP']['dbNSFP_Polyphen2_HDIV_rankscore']
                    variant_obj.Polyphen2_HDIV_pred = variant['dbNSFP']['dbNSFP_Polyphen2_HDIV_pred']
                    variant_obj.Polyphen2_HVAR_score = variant['dbNSFP']['dbNSFP_Polyphen2_HVAR_score']
                    variant_obj.Polyphen2_HVAR_rankscore = variant['dbNSFP']['dbNSFP_Polyphen2_HVAR_rankscore']
                    variant_obj.Polyphen2_HVAR_pred = variant['dbNSFP']['dbNSFP_Polyphen2_HVAR_pred']
                    variant_obj.LRT_score = variant['dbNSFP']['dbNSFP_LRT_score']
                    variant_obj.LRT_converted_rankscore = variant['dbNSFP']['dbNSFP_LRT_converted_rankscore']
                    variant_obj.LRT_pred = variant['dbNSFP']['dbNSFP_LRT_pred']
                    variant_obj.LRT_Omega = variant['dbNSFP']['dbNSFP_LRT_Omega']
                    variant_obj.MutationTaster_score = variant['dbNSFP']['dbNSFP_MutationTaster_score']
                    variant_obj.MutationTaster_converted_rankscore = variant['dbNSFP']['dbNSFP_MutationTaster_converted_rankscore']
                    variant_obj.MutationTaster_pred = variant['dbNSFP']['dbNSFP_MutationTaster_pred']
                    variant_obj.MutationTaster_model = variant['dbNSFP']['dbNSFP_MutationTaster_model']
                    variant_obj.MutationTaster_AAE = variant['dbNSFP']['dbNSFP_MutationTaster_AAE']
                    variant_obj.MutationAssessor_UniprotID = variant['dbNSFP']['dbNSFP_MutationAssessor_UniprotID']
                    variant_obj.MutationAssessor_variant = variant['dbNSFP']['dbNSFP_MutationAssessor_variant']
                    variant_obj.MutationAssessor_score = variant['dbNSFP']['dbNSFP_MutationAssessor_score']
                    variant_obj.MutationAssessor_rankscore = variant['dbNSFP']['dbNSFP_MutationAssessor_rankscore']
                    variant_obj.MutationAssessor_pred = variant['dbNSFP']['dbNSFP_MutationAssessor_pred']
                    variant_obj.FATHMM_score = variant['dbNSFP']['dbNSFP_FATHMM_score']
                    variant_obj.FATHMM_converted_rankscore = variant['dbNSFP']['dbNSFP_FATHMM_converted_rankscore']
                    variant_obj.FATHMM_pred = variant['dbNSFP']['dbNSFP_FATHMM_pred']
                    variant_obj.PROVEAN_score = variant['dbNSFP']['dbNSFP_PROVEAN_score']
                    variant_obj.PROVEAN_converted_rankscore = variant['dbNSFP']['dbNSFP_PROVEAN_converted_rankscore']
                    variant_obj.PROVEAN_pred = variant['dbNSFP']['dbNSFP_PROVEAN_pred']
                    variant_obj.Transcript_id_VEST3 = variant['dbNSFP']['dbNSFP_Transcript_id_VEST3']
                    variant_obj.Transcript_var_VEST3 = variant['dbNSFP']['dbNSFP_Transcript_var_VEST3']
                    variant_obj.VEST3_score = variant['dbNSFP']['dbNSFP_VEST3_score']
                    variant_obj.VEST3_rankscore = variant['dbNSFP']['dbNSFP_VEST3_rankscore']
                    variant_obj.MetaSVM_score = variant['dbNSFP']['dbNSFP_MetaSVM_score']
                    variant_obj.MetaSVM_rankscore = variant['dbNSFP']['dbNSFP_MetaSVM_rankscore']
                    variant_obj.MetaSVM_pred = variant['dbNSFP']['dbNSFP_MetaSVM_pred']
                    variant_obj.MetaLR_score = variant['dbNSFP']['dbNSFP_MetaLR_score']
                    variant_obj.MetaLR_rankscore = variant['dbNSFP']['dbNSFP_MetaLR_rankscore']
                    variant_obj.MetaLR_pred = variant['dbNSFP']['dbNSFP_MetaLR_pred']
                    variant_obj.Reliability_index = variant['dbNSFP']['dbNSFP_Reliability_index']
                    variant_obj.CADD_raw = variant['dbNSFP']['dbNSFP_CADD_raw']
                    variant_obj.CADD_raw_rankscore = variant['dbNSFP']['dbNSFP_CADD_raw_rankscore']
                    variant_obj.CADD_phred = variant['dbNSFP']['dbNSFP_CADD_phred']
                    variant_obj.DANN_score = variant['dbNSFP']['dbNSFP_DANN_score']
                    variant_obj.DANN_rankscore = variant['dbNSFP']['dbNSFP_DANN_rankscore']
                    variant_obj.fathmm_MKL_coding_score = variant['dbNSFP']['dbNSFP_fathmm-MKL_coding_score']
                    variant_obj.fathmm_MKL_coding_rankscore = variant['dbNSFP']['dbNSFP_fathmm-MKL_coding_rankscore']
                    variant_obj.fathmm_MKL_coding_pred = variant['dbNSFP']['dbNSFP_fathmm-MKL_coding_pred']
                    variant_obj.fathmm_MKL_coding_group = variant['dbNSFP']['dbNSFP_fathmm-MKL_coding_group']
                    variant_obj.Eigen_raw = variant['dbNSFP']['dbNSFP_Eigen-raw']
                    variant_obj.Eigen_phred = variant['dbNSFP']['dbNSFP_Eigen-phred']
                    # variant_obj.Eigen_raw_rankscore = variant['dbNSFP']['dbNSFP_Eigen-raw_rankscore']
                    variant_obj.Eigen_PC_raw = variant['dbNSFP']['dbNSFP_Eigen-PC-raw']
                    variant_obj.Eigen_PC_raw_rankscore = variant['dbNSFP']['dbNSFP_Eigen-PC-raw_rankscore']
                    variant_obj.GenoCanyon_score = variant['dbNSFP']['dbNSFP_GenoCanyon_score']
                    variant_obj.GenoCanyon_score_rankscore = variant['dbNSFP']['dbNSFP_GenoCanyon_score_rankscore']
                    variant_obj.integrated_fitCons_score = variant['dbNSFP']['dbNSFP_integrated_fitCons_score']
                    variant_obj.integrated_fitCons_rankscore = variant['dbNSFP']['dbNSFP_integrated_fitCons_rankscore']
                    variant_obj.integrated_confidence_value = variant['dbNSFP']['dbNSFP_integrated_confidence_value']
                    variant_obj.GM12878_fitCons_score = variant['dbNSFP']['dbNSFP_GM12878_fitCons_score']
                    variant_obj.GM12878_fitCons_rankscore = variant['dbNSFP']['dbNSFP_GM12878_fitCons_rankscore']
                    variant_obj.GM12878_confidence_value = variant['dbNSFP']['dbNSFP_GM12878_confidence_value']
                    variant_obj.H1_hESC_fitCons_score = variant['dbNSFP']['dbNSFP_H1-hESC_fitCons_score']
                    variant_obj.H1_hESC_fitCons_rankscore = variant['dbNSFP']['dbNSFP_H1-hESC_fitCons_rankscore']
                    variant_obj.H1_hESC_confidence_value = variant['dbNSFP']['dbNSFP_H1-hESC_confidence_value']
                    variant_obj.HUVEC_fitCons_score = variant['dbNSFP']['dbNSFP_HUVEC_fitCons_score']
                    variant_obj.HUVEC_fitCons_rankscore = variant['dbNSFP']['dbNSFP_HUVEC_fitCons_rankscore']
                    # variant_obj.HUVEC_confidence_value = variant['dbNSFP']['dbNSFP_HUVEC_confidence_value']
                    # variant_obj.GERP_NR = variant['dbNSFP']['dbNSFP_GERP++_NR']
                    # variant_obj.GERP_RS = variant['dbNSFP']['dbNSFP_GERP++_RS']
                    # variant_obj.GERP_RS_rankscore = variant['dbNSFP']['dbNSFP_GERP++_RS_rankscore']
                    # variant_obj.phyloP100way_vertebrate = variant['dbNSFP']['dbNSFP_phyloP100way_vertebrate']
                    # variant_obj.phyloP100way_vertebrate_rankscore = variant['dbNSFP']['dbNSFP_phyloP100way_vertebrate_rankscore']
                    # variant_obj.phyloP20way_mammalian = variant['dbNSFP']['dbNSFP_phyloP20way_mammalian']
                    # variant_obj.phyloP20way_mammalian_rankscore = variant['dbNSFP']['dbNSFP_phyloP20way_mammalian_rankscore']
                    # variant_obj.phastCons100way_vertebrate = variant['dbNSFP']['dbNSFP_phastCons100way_vertebrate']
                    # variant_obj.phastCons100way_vertebrate_rankscore = variant['dbNSFP']['dbNSFP_phastCons100way_vertebrate_rankscore']
                    # variant_obj.phastCons20way_mammalian = variant['dbNSFP']['dbNSFP_phastCons20way_mammalian']
                    # variant_obj.phastCons20way_mammalian_rankscore = variant['dbNSFP']['dbNSFP_phastCons20way_mammalian_rankscore']
                    # variant_obj.SiPhy_29way_pi = variant['dbNSFP']['dbNSFP_SiPhy_29way_pi']
                    # variant_obj.SiPhy_29way_logOdds = variant['dbNSFP']['dbNSFP_SiPhy_29way_logOdds']
                    # variant_obj.SiPhy_29way_logOdds_rankscore = variant['dbNSFP']['dbNSFP_SiPhy_29way_logOdds_rankscore']
                    variant_obj.clinvar_rs = variant['dbNSFP']['dbNSFP_clinvar_rs']
                    variant_obj.clinvar_clnsig = variant['dbNSFP']['dbNSFP_clinvar_clnsig']
                    variant_obj.clinvar_trait = variant['dbNSFP']['dbNSFP_clinvar_trait']
                    variant_obj.clinvar_golden_stars = variant['dbNSFP']['dbNSFP_clinvar_golden_stars']
                    variant_obj.mcap_score = variant['mcap']
                    variant_obj.mcap_rankscore = variant['dbNSFP']['dbNSFP_M-CAP_rankscore']
                    variant_obj.mcap_pred = variant['dbNSFP']['dbNSFP_M-CAP_pred']
                    variant_obj.revel_score = variant['dbNSFP']['dbNSFP_REVEL_score']

                variants.append(variant_obj)
                # print 'query', variant_obj.query
                # print(variant['chr'], variant['pos'])
                # variant_obj.save()
    Variant.objects.bulk_create(variants)

    stop = datetime.datetime.now()
    elapsed = stop - start

    individual.insertion_time = elapsed


    individual.status = 'populated'
    individual.n_lines = count2
    individual.save()

    stop = datetime.datetime.now()
    task.finished = stop
    task.status = 'populated'
    task.save()

    # message = """
    #         The individual %s was inserted to the database with success!
    #         Now you can check the variants on the link: \n
    #         http://mendelmd.org/individuals/view/%s
    #             """ % (individual.name, individual.id)

    print('Individual %s Populated!' % (individual.id))

    command = 'rm -rf %s' % (task_location)
    run(command, shell=True)

    # command = 'rm -rf %s/ann_sample' % (filepath)
    # os.system(command)
