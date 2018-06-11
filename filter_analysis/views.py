from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Min, Max
from django.core import serializers
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse

#from django.contrib.formtools.wizard import FormWizard
# from django.contrib.formtools.wizard.views import SessionWizardView

from .forms import FilterWiZardForm1, FilterWiZardForm2, FilterWiZardForm3, FamilyAnalysisForm
from datetime import datetime
import operator
from django.conf import settings
from .forms import *
import csv
import pickle

from individuals.models import *
from filter_analysis.forms import *
from filter_analysis.models import *
from genes.models import GeneGroup, Gene, CGDEntry, GeneList

from .filter_options import *

from diseases.models import Disease, HGMDGene, HGMDPhenotype
from diseases.models import Gene as GeneDisease

import json

from django.shortcuts import render

# import django_tables2 as tables
# from django_tables2 import RequestConfig

#a method to integrate all different filters
#should return an object with all the results

def test(request):
    form = FilterAnalysisForm(request.user)

    return render(request, 'filter_analysis/test.html', {'form':form});


def oneclick(request):
    form = FilterAnalysisForm(request.user)
    if request.method == 'GET':
        # print request.META
        query_string = request.META['QUERY_STRING']
        # print(query_string)
        if query_string != '':
            new_query_string = []
            query_string = query_string.split('&')
            for item in query_string:
                if not (item.startswith('csrfmiddlewaretoken') or item.startswith('hash') or item.startswith('wizard')):
                    #get here only the ones need to be cleaned Ex. 1-chr
                    #item = "-".join(item.split('-', 2)[1:])
                    new_query_string.append(item)

            #create new query
            filterstring = "&".join(new_query_string)
            return redirect(reverse('filter_analysis')+'?'+filterstring)

    return render(request, 'filter_analysis/oneclick.html', {'form':form});


def calculate_summary(step, args, query, exclude):

    print('enter calculate summary')    
    summary = {}
    summary[step] = {}

    # 1) calculate number of variants
    variants = Variant.objects.filter(*args, **query).exclude(**exclude)
    n_variants = variants.count()#.prefetch_related('individual')
    summary[step]['variants'] = n_variants
    
    #2)Calculate number of genes
    genes = variants.values_list('gene', flat=True)
    genes = sorted(list(set(genes)))

    summary[step]['genes'] = len(genes)

    #3)Calculate number of genes at omim
    queries = [Q(genes__icontains=value) for value in list(genes)]
    if len(queries) > 0:
        query = queries.pop()
        for item in queries:
            query |= item
        summary[step]['genes_at_omim'] = GeneDisease.objects.filter(official_name__in=list(genes)).count()#query
    else:
        summary[step]['genes_at_omim'] = '-'
    

    print('exit calculate summary')

    return summary

#show all steps from filter analysis 
def filter_analysis_table(request):
    print('dynamic filter analysis')
    results = {}
    
    query = {}
    exclude = {}
    summary = {}
    args = []

    table_list = []

    form = FilterAnalysisForm(request.user, request.GET)

    filter_by_individuals(request, args, query, exclude)

    table_list.append(calculate_summary('initial', args, query, exclude))

    #CHR
    filter_chr(request, query)
    #pos
    filter_pos(request, query)
    #snp_list
    filter_snp_list(request, query)
    #Gene List, this is entered by hand
    filter_gene_list(request, query, args)
    #Inheritance_model
    filter_mutation_type(request, args)

    table_list.append(calculate_summary('mutation_type', args, query, exclude))

    #Clinical
    filter_cln(request, query)
    #Variant type SNP EFF       
    filter_variant_type_snpeff(request, query)
    #DBSNP
    filter_dbsnp(request, query)
    #1000genomes
    filter_by_1000g(request, args)
    #dbsnp Freq
    filter_by_dbsnp(request, args)
    #Exome Variation Server Freq
    filter_by_esp(request, args)
    #hi score
    # filter_by_hi_score(request, args)
    #SIFT
    filter_by_sift(request, args)
    #POLYPHEN
    filter_by_pp2(request, args)
    filter_by_cadd(request, args)
    filter_by_mcap(request, args)
    filter_by_rf_score(request, args)
    filter_by_ada_score(request, args)

    filter_by_segdup(request, args)
    #filter by disease databases
    filter_omim(request, args)
    filter_cgd(request, args)
    filter_hgmd(request, args)
    filter_genelists(request, query, args, exclude)
    #DBSNP Build
    filter_dbsnp_build(request, args)            
    #Read Depth
    filter_read_depth(request, args)            
    filter_qual(request, args)
    filter_filter(request, query)
    #Functional class
    filter_func_class(request, query)
    #IMPACT
    filter_impact(request, query)
    
    # filter_by_individuals_full(request, args, query, exclude)

    #last call to the DATABASE Finally!!!!!! 
    variants = Variant.objects.filter(*args, **query).exclude(**exclude).prefetch_related('individual')

    table_list.append(calculate_summary('final', args, query, exclude))

    #summary
    summary['genes'] = variants.values_list('gene', flat=True)
    summary['genes'] = sorted(list(set(summary['genes'])))
    summary['n_genes'] =  len(summary['genes'])
    summary['has_variants'] = True
    
    #show summary of genes associated with diseases every time
    #if summary['n_genes'] < 500:

    genes = Gene.objects.filter(symbol__in=list(summary['genes'])).values('symbol', 'diseases').prefetch_related('diseases')                
    genes_hgmd = HGMDGene.objects.filter(symbol__in=list(summary['genes'])).prefetch_related('diseases')# | reduce(lambda x, y: x | y, [Q(aliases__icontains=word) for word in list(summary['genes'])]))
    #return Disease.objects.filter(Q(name__icontains=name)|Q(genes__icontains=name))
    #for each gene name create a query
    queries = [Q(genes__icontains=value) for value in list(summary['genes'])]
    if len(queries) > 0:
        query = queries.pop()
        for item in queries:
            query |= item
        genes_omim = GeneDisease.objects.filter(official_name__in=list(summary['genes'])).prefetch_related('diseases').order_by('official_name')#query
    else:
        genes_omim = []
    #get genes at CGD
    genes_cgd = CGDEntry.objects.filter(GENE__in=list(summary['genes'])).prefetch_related('CONDITIONS')

    # else:
    #     genes = []
    #     genes_hgmd = []
    #     genes_omim = []
    #     genes_cgd = []

    summary['n_variants'] = len(variants)

    # 'variants':variants, 
    #     'form':form, 
    #     'summary':summary, 
    #     'query_string':query_string, 
    #     'filteranalysis':filteranalysis, 
    #     'filterconfigs':filterconfigs, 
    #     'genes':genes, 
    #     'genes_hgmd':genes_hgmd,
    #     'genes_omim':genes_omim,
    #     'genes_cgd':genes_cgd
    #return results

    table = table_list

    return render(request, 'filter_analysis/table.html', 
        {'table':table})



def filter_analysis(request,query, args, exclude):
    '''
    This function receives request and returns a dictionary with the variants
    '''
    # print('filter analysis')

    #CHR
    filter_chr(request, query)
    #pos
    filter_pos(request, query)
    #snp_list
    filter_snp_list(request, query, exclude)

    #Gene List, this is entered by hand
    filter_gene_list(request, query, args)
    #Mutation Type
    filter_mutation_type(request, args)
    #Variant type SNP EFF       
    filter_effect(request, query)
    #Exclude variants at dbsnp
    filter_dbsnp(request, query)

    filter_varisnp(request, query, exclude)
    # print 'exclude debug1', exclude

    #1000genomes
    filter_by_1000g(request, args)
    #dbsnp Freq
    filter_by_dbsnp(request, args)
    #Exome Variation Server Freq
    filter_by_esp(request, args)

    #SIFT
    filter_by_sift(request, args)
    #POLYPHEN
    filter_by_pp2(request, args)
    filter_by_cadd(request, args)
    filter_by_mcap(request, args)
    filter_by_rf_score(request, args)
    filter_by_ada_score(request, args)
    
    #filter by disease databases
    filter_omim(request, args)
    filter_cgd(request, args)
    filter_hgmd(request, args)
    filter_genelists(request, query, args, exclude)
    #DBSNP Build
    filter_dbsnp_build(request, args)            
    #Read Depth
    filter_read_depth(request, args)            
    filter_qual(request, args)
    filter_filter(request, query)
    #Functional class
    filter_func_class(request, query)
    #IMPACT
    filter_impact(request, query)
    filter_is_at_hgmd(request, query)
    filter_clnsig(request, query)

    # filter_individuals(request, query)
    
    # filter_by_individuals(request, *query, *args, *exclude)

def get_genes(summary):

    genes ={}

    genes['genes'] = Gene.objects.filter(symbol__in=list(summary['genes'])).values('symbol', 'diseases').prefetch_related('diseases')                
    
    genes['genes_hgmd'] = HGMDGene.objects.filter(symbol__in=list(summary['genes'])).prefetch_related('diseases')

    #for each gene name create a query
    queries = [Q(genes__icontains=value) for value in list(summary['genes'])]
    if len(queries) > 0:
        query = queries.pop()
        for item in queries:
            query |= item
        genes['genes_omim'] = GeneDisease.objects.filter(official_name__in=list(summary['genes'])).prefetch_related('diseases').order_by('official_name')#query
    else:
        genes['genes_omim'] = []
    #get genes at CGD
    genes['genes_cgd'] = CGDEntry.objects.filter(GENE__in=list(summary['genes'])).prefetch_related('CONDITIONS').order_by('GENE')

    return genes

#This is the most important function
def index(request):
    query = {}
    exclude = {}
    summary = {}
    args = []

    #this removes page from QUERY_STRING
    query_string = request.META['QUERY_STRING']
    new_query_string = []
    for item in query_string.split('&'):
        if not item.startswith('page'):
             new_query_string.append(item)
    query_string = "&".join(new_query_string)
    
    # print 'query string'
    # print query_string 
    
    filteranalysis = FilterAnalysis.objects.all().prefetch_related('user')
    filterconfigs = FilterConfig.objects.all().prefetch_related('user')
    
    #this is for checking if query is empty (to avoid loading at the first time)
    if query_string != [''] and query_string != '' :
        
        #make it GET for explicit urls
        if request.method == 'GET':

            form = FilterAnalysisForm(request.user, request.GET)

            if 'sort_by' in request.GET:
                sort_by = request.GET['sort_by']
                if sort_by == 'desc':
                    sort = 'asc'
                else:
                    sort = 'desc'
            else:
                sort = 'asc'

            if 'order_by' in request.GET:
                if sort_by == 'desc':
                    order_by = '-%s' % request.GET['order_by']
                else:
                    order_by = request.GET['order_by']
            else:
                order_by = 'gene'

            filter_analysis(request, query, args, exclude)

            individuals_list = filter_individuals_variants(request, query, args, exclude)

            if len(individuals_list) > 0:
                #only add to query after filtering the indexes 
                query['individual_id__in'] = individuals_list

                filter_variants_per_gene(request, query, args, exclude)
                filter_genes_in_common(request, query, args, exclude)
                filter_positions_in_common(request, query, args, exclude)
            
            # print('exclude keys', list(exclude.keys()))
            #last call to the DATABASE Finally!!!!!! 
            variants = Variant.objects.filter(*args, **query).exclude(**exclude).prefetch_related('individual').order_by(order_by)
            
            #export_to_csv(request, variants)
            export = request.GET.get('export', '')
            if export != '':
                if export == 'csv':
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename=export.csv'
                    writer = csv.writer(response)
                    
                elif export == 'txt':
                    response = HttpResponse(content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename=export.txt'
                    writer = csv.writer(response, delimiter='\t', quoting=csv.QUOTE_NONE)    
                writer.writerow(['Individual', 'Index', 'Pos_index', 'Chr', 'Pos', 'Variant_id', 'Ref', 'Alt', 'Qual', 'Filter', 'Info', 'Format', 'Genotype_col', 'Genotype', 'Read_depth', 'Gene', 'Mutation_type', 'Vartype', 'Genomes1k_maf', 'Dbsnp_maf', 'Esp_maf', 'Dbsnp_build', 'Sift', 'Sift_pred', 'Polyphen2', 'Polyphen2_pred', 'Condel', 'Condel_pred', 'DANN', 'CADD', 'Is_at_omim', 'Is_at_hgmd', 'Hgmd_entries', 'Effect', 'Impact', 'Func_class', 'Codon_change', 'Aa_change', 'Gene_name', 'Biotype', 'Gene_coding', 'Transcript_id', 'Exon_rank', 'Allele', 'Gene', 'Feature', 'Feature_type', 'Consequence', 'Cdna_position', 'Cds_position', 'Protein_position', 'Amino_acids', 'Codons', 'Existing_variation', 'Distance', 'Strand', 'Symbol', 'Symbol_source', 'Sift', 'Polyphen', 'Condel']) 
                for variant in variants:
                    # print 'variant', variant.index
                    writer.writerow([variant.individual, variant.index, variant.pos_index, variant.chr, variant.pos, variant.variant_id, variant.ref, variant.alt, variant.qual, variant.filter, json.loads(variant.info), variant.format, variant.genotype_col, variant.genotype, variant.read_depth, variant.gene, variant.mutation_type, variant.vartype, variant.genomes1k_maf, variant.dbsnp_maf, variant.esp_maf, variant.dbsnp_build, variant.sift, variant.sift_pred, variant.polyphen2, variant.polyphen2_pred, variant.condel, variant.condel_pred, variant.dann, variant.cadd, variant.is_at_omim, variant.is_at_hgmd, variant.hgmd_entries, variant.snpeff_effect, variant.snpeff_impact, variant.snpeff_func_class, variant.snpeff_codon_change, variant.snpeff_aa_change, variant.snpeff_gene_name, variant.snpeff_biotype, variant.snpeff_gene_coding, variant.snpeff_transcript_id, variant.snpeff_exon_rank, variant.vep_allele, variant.vep_gene, variant.vep_feature, variant.vep_feature_type, variant.vep_consequence, variant.vep_cdna_position, variant.vep_cds_position, variant.vep_protein_position, variant.vep_amino_acids, variant.vep_codons, variant.vep_existing_variation, variant.vep_distance, variant.vep_strand, variant.vep_symbol, variant.vep_symbol_source, variant.vep_sift, variant.vep_polyphen, variant.vep_condel])
                return response

            #summary
            summary['genes'] = variants.values_list('gene', flat=True)
            # print(summary['genes'])
            summary['genes'] = list(set(summary['genes']))
            summary['genes'] = sorted(list(filter(None.__ne__, summary['genes'])))
            summary['n_genes'] =  len(summary['genes'])
            summary['has_variants'] = True
            summary['n_variants'] = len(variants)

            genes = get_genes(summary)            

            paginator = Paginator(variants, 100) # Show 25 contacts per page
            try:
               page = int(request.GET.get('page', '1'))
            except ValueError:
               page = 1
            try:
               variants = paginator.page(page)
            except PageNotAnInteger:
               # If page is not an integer, deliver first page.
               variants = paginator.page(1)
            except EmptyPage:
               # If page is out of range (e.g. 9999), deliver last page of results.
               variants = paginator.page(paginator.num_pages)
    #first entrance in methods
    else:
        variants = []
        summary = {}
        genes = {}

        summary['has_variants'] = False
        #fake number just not to open accordion on view 
        summary['n_genes'] = 1000
        
        genes['genes'] = []
        genes['genes_hgmd'] = []
        genes['genes_omim'] = []
        genes['genes_cgd'] = []
        form = FilterAnalysisForm(request.user)



    # print(summary)
    return render(request, 'filteranalysis/index.html', 
        {'variants':variants, 
        'form':form, 
        'summary':summary,
        'query_string':query_string, 
        'filteranalysis':filteranalysis, 
        'filterconfigs':filterconfigs, 
        'genes':genes['genes'], 
        'genes_hgmd':genes['genes_hgmd'],
        'genes_omim':genes['genes_omim'],
        'genes_cgd':genes['genes_cgd']})


def filter_family_analysis(request, query, args, exclude):

    print('Get family variants')
    father = request.GET.get('father', '')
    mother = request.GET.get('mother', '')
    

    parents_variants = {'father':{}, 'mother':{}}
    parents_list = []
    parents = {}
    if father != '':
        parents['father']=father
        parents_list.append(father)
    if mother != '':
        parents['mother']=mother
        parents_list.append(mother)
    # print 'parents', parents            
        
    # parents = {'father':father, 'mother':mother}
    # query_bkp = query['individual_id__in']
    #for each parent get variants from parents and build dict for future filtering
    parents_indexes = Variant.objects.filter(individual__id__in=parents_list).values_list('index', flat=True)
    parents_positions = Variant.objects.filter(individual__id__in=parents_list).values_list('pos_index', flat=True)

    print('parents_indexes', len(parents_indexes), parents_indexes)
    for individual in parents:
        query['individual_id__in'] = [parents[individual]]
        #parents_variants[individual] = Variant.objects.filter(individual__id=parents[individual], *args, **query).exclude(**exclude)#.values_list('index', flat=True)
        #print 'parents_variants', len(parents_variants[individual])
        individual_variants = Variant.objects.filter(individual__id=parents[individual]).values('chr', 'pos', 'mutation_type', 'gene')
        print('individual variants')
        print(individual, parents[individual])
        print(len(individual_variants)) #all right
        for variant in individual_variants:
            id = '%s-%s' % (variant['chr'], variant['pos'])
            gene = variant['gene']
            #check if gene don't exists in structure first time of gene in structure 
            if gene not in parents_variants[individual]:
                parents_variants[individual][gene] = {}
            parents_variants[individual][gene][id] = {}
            parents_variants[individual][gene][id][variant['mutation_type']] = 0

    children = request.GET.getlist('children')

    children_indexes = Variant.objects.filter(individual__id__in=children).values_list('index', flat=True)
    children_positions = Variant.objects.filter(individual__id__in=children).values_list('pos_index', flat=True)
    #build same dict for children
    print('debug argments', args, query, exclude)
    children_variants = {}
    for child in children:
        print('child', child)
        children_variants[child] = {}
        query['individual_id__in'] = child
        individual_variants = Variant.objects.filter(individual__id=child, *args, **query).exclude(**exclude).values('id', 'chr', 'pos', 'genotype', 'gene')
        print('query', individual_variants.query)
        for variant in individual_variants:
            id = '%s-%s' % (variant['chr'], variant['pos'])
            gene = variant['gene']
            #check if gene don't exists in structure first time of gene in structure 
            if gene not in children_variants[child]:
                children_variants[child][gene] = {}
            children_variants[child][gene][id] = {}
            children_variants[child][gene][id][variant['genotype']] = variant['id']
        print('finished build dict')

    # print 'children_variants', children_variants


    
    inheritance_option = request.GET.get('inheritance_option', '')
    
    # variants = Variant.objects.filter(*args, **query).exclude(**exclude)
    # implement recessive model
    if inheritance_option == 'recessive' or inheritance_option == 'xlinked recessive':
        #this guarantee that same genotype is not at parents
        # args.append(~Q(index__in=parents_indexes))
        #even more efficient add only index that are not present at childs, this will save a lot of query time!
        index_list = []
        # for parent_index in parents_indexes:
        #     if parent_index not in children_indexes:
        #         index_list.append(parent_index)
        # print 'index_list recessive', len(children_indexes)
        # print 'index_list parents', len(parents_indexes)
        # args.append(Q(index__in=index_list))
        index_list = list(set(children_indexes)-set(parents_indexes))
        # print 'index_list', len(index_list)
        args.append(Q(index__in=index_list))

        #ex instead of adding 83k indexes from parents will add only the ones not present at child
    elif inheritance_option == 'recessive denovo':
        #this should guarantee that both parents are genotyped and do not have the variants
        args.append(~Q(pos_index__in=parents_positions))
        #should be
        #args.append(Q(pos_index__in=parents_positions))
        #args.append(~Q(index__in=parents_indexes))
    elif inheritance_option == 'dominant' or inheritance_option == 'xlinked dominant':
        #this is very inefficient
        # args.append(~Q(pos_index__in=parents_positions))
        
        positions_list = list(set(children_positions)-set(parents_positions))
        args.append(Q(pos_index__in=positions_list))



    elif inheritance_option == 'compound heterozygous':
        print('doing compound heterozygous')
        #build children dict with genes and variants
        
        #now search for compound heterozygous magic happens in here!
        exclude_gene_list =[]
        exclude_variant_list=[]
        # print 'opps erro no children'
        # print children
        for child in children:
            #for every gene
            for gene in children_variants[child]:
                #check if at least one variant comes unique from father 
                #and one comes unique from mother
                one_comes_only_from_father = False
                one_comes_only_from_mother = False
                #for every variant in gene from child
                #3 possibilities 
                #two denovo
                #one denovo one from father or mother
                #one from father and one from mother
                if gene in parents_variants['father'] and gene in parents_variants['mother']:
                    # if gene == 'KIF14':
                    #     print 'achou KIF14'
                    #     print child
                    #     print children_variants[child][gene]
                    #     print parents_variants['father'][gene]
                    #     print parents_variants['mother'][gene]
                    #for every variant in child gene
                    for id in children_variants[child][gene]:

                        if (id in parents_variants['father'][gene]) and (id not in parents_variants['mother'][gene]):
                            if 'HOM' not in parents_variants['father'][gene][id]:
                                one_comes_only_from_father = True
                        if (id in parents_variants['mother'][gene]) and (id not in parents_variants['father'][gene]):
                            if 'HOM' not in parents_variants['mother'][gene][id]:
                                one_comes_only_from_mother = True


                        if id in parents_variants['mother'][gene]:
                            if 'HOM' in parents_variants['mother'][gene][id]:
                                exclude_variant_list.append(list(children_variants[child][gene][id].values())[0])
                        if id in parents_variants['father'][gene]:
                            if 'HOM' in parents_variants['father'][gene][id]:
                                exclude_variant_list.append(list(children_variants[child][gene][id].values())[0])
                        #if present in both exclude variants
                        # if remove_in_both_parents == 'on':
                        if (id in parents_variants['father'][gene]) and (id in parents_variants['mother'][gene]):
                            # print 'variant id to remove', children_variants[child][gene][id].values()[0]
                            exclude_variant_list.append(list(children_variants[child][gene][id].values())[0])

                        #if id not seeing in both parents remove from results
                        # if remove_not_in_parents== 'on':
                        #     if id not in parents_variants['mother'][gene]:
                        #         if id not in parents_variants['father'][gene]:
                        #             # print 'Exclui variant %s' % (id)
                        #             exclude_variant_list.append(children_variants[child][gene][id].values()[0])
                    if one_comes_only_from_father and one_comes_only_from_mother:
                        pass
                    else:
                        exclude_gene_list.append(gene)
                #option for removing variants from genes not seing in parents
                else:
                #     if remove_not_in_parents == 'on':
                    exclude_gene_list.append(gene)
                
        print(len(exclude_gene_list))
        if 'gene__in' in exclude:
            exclude['gene__in'] = exclude['gene__in']+exclude_gene_list
        else:
            exclude['gene__in'] = exclude_gene_list
        
        args.append(~Q(id__in=exclude_variant_list))
#       


    return parents_variants
        # print 'parents_variants', parents_variants
    # query['individual_id__in'] = query_bkp

def fill_parents_variants(request, variants, children_positions, parents_variants):

    
    # father = request.GET.get('father', '')
    # mother = request.GET.get('mother', '')
    
    # print 'children_positions', children_positions.count()

    # parents_variants = {'father':{}, 'mother':{}}

    # parents = {}
    # if father != '':
    #     parents['father']=father
    # if mother != '':
    #     parents['mother']=mother


    # #get a small postion of variants from father
    # parents_variants = {'father':{}, 'mother':{}}
    # print 'get position from parents'
    # for individual in parents:
        
    #     individual_variants = Variant.objects.filter(individual__id=parents[individual], pos_index__in=children_positions).values('chr', 'pos', 'mutation_type', 'gene')
    #     print 'parent variants'
    #     print individual, parents[individual]
    #     print len(individual_variants) #all right
    #     for variant in individual_variants:
    #         id = '%s-%s' % (variant['chr'], variant['pos'])
    #         gene = variant['gene']
    #         #check if gene don't exists in structure first time of gene in structure 
    #         if gene not in parents_variants[individual]:
    #             parents_variants[individual][gene] = {}
    #         parents_variants[individual][gene][id] = {}
    #         parents_variants[individual][gene][id][variant['mutation_type']] = 0
    # print 'get position from childs'
    for variant in variants:
        id = '%s-%s' % (variant.chr, variant.pos)
        gene = variant.gene
        if gene in  parents_variants['father']:
            if id in parents_variants['father'][gene]:
                variant.father =  list(parents_variants['father'][gene][id].keys())[0]
        if gene in  parents_variants['mother']:
            if id in parents_variants['mother'][gene]:
                variant.mother =  list(parents_variants['mother'][gene][id].keys())[0]    
    # print 'pass'
#This is the most important function
def family_analysis(request):
    query = {}
    exclude = {}
    summary = {}
    args = []

    #this removes page from QUERY_STRING
    query_string = request.META['QUERY_STRING']
    new_query_string = []
    for item in query_string.split('&'):
        if not item.startswith('page'):
             new_query_string.append(item)
    query_string = "&".join(new_query_string)
    
    # print 'query string'
    # print query_string 
    
    filteranalysis = FilterAnalysis.objects.all().prefetch_related('user')
    filterconfigs = FilterConfig.objects.all().prefetch_related('user')
    
    #this is for checking if query is empty (to avoid loading at the first time)
    if query_string != [''] and query_string != '' :
        
        #make it GET for explicit urls
        if request.method == 'GET':

            form = FamilyAnalysisForm(request.user, request.GET)
            # request.GET = request.GET.copy()

            if 'sort_by' in request.GET:
                sort_by = request.GET['sort_by']
                if sort_by == 'desc':
                    sort = 'asc'
                else:
                    sort = 'desc'
            else:
                sort = 'asc'

            if 'order_by' in request.GET:
                if sort_by == 'desc':
                    order_by = '-%s' % request.GET['order_by']
                else:
                    order_by = request.GET['order_by']
            else:
                order_by = 'gene'

            filter_analysis(request, query, args, exclude)

            individuals_list = filter_individuals_variants(request, query, args, exclude)            

            parents_variants = filter_family_analysis(request, query, args, exclude)

            children = request.GET.getlist('children')
            if len(children) > 0:
                for child in children:
                    individuals_list.append(child)

            if len(individuals_list) > 0:
                #only add to query after filtering the indexes 
                query['individual_id__in'] = individuals_list

                filter_variants_per_gene(request, query, args, exclude)
                filter_genes_in_common(request, query, args, exclude)
                filter_positions_in_common(request, query, args, exclude)
            
            

            #last call to the DATABASE Finally!!!!!! 
            print('last call to database')
            variants = Variant.objects.filter(*args, **query).exclude(**exclude).prefetch_related('individual').order_by(order_by)

            #child_positions
            children_positions = Variant.objects.filter(*args, **query).exclude(**exclude).values_list('pos_index', flat=True)
            
            # export_to_csv()
            print('fill parents variants')
            fill_parents_variants(request, variants, children_positions, parents_variants)
            
            export = request.GET.get('export', '')
            if export != '':
                if export == 'csv':
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename=export.csv'
                    writer = csv.writer(response)
                    
                elif export == 'txt':
                    response = HttpResponse(content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename=export.txt'
                    writer = csv.writer(response, delimiter='\t', quoting=csv.QUOTE_NONE)    
                writer.writerow(['Individual', 'Index', 'Pos_index', 'Chr', 'Pos', 'Variant_id', 'Ref', 'Alt', 'Qual', 'Filter', 'Info', 'Format', 'Genotype_col', 'Genotype', 'Father Genotype', 'Mother Genotype', 'Read_depth', 'Gene', 'Mutation_type', 'Vartype', 'Genomes1k_maf', 'Dbsnp_maf', 'Esp_maf', 'Dbsnp_build', 'Sift', 'Sift_pred', 'Polyphen2', 'Polyphen2_pred', 'Condel', 'Condel_pred', 'DANN', 'CADD', 'Is_at_omim', 'Is_at_hgmd', 'Hgmd_entries', 'Effect', 'Impact', 'Func_class', 'Codon_change', 'Aa_change', 'Gene_name', 'Biotype', 'Gene_coding', 'Transcript_id', 'Exon_rank', 'Allele', 'Gene', 'Feature', 'Feature_type', 'Consequence', 'Cdna_position', 'Cds_position', 'Protein_position', 'Amino_acids', 'Codons', 'Existing_variation', 'Distance', 'Strand', 'Symbol', 'Symbol_source', 'Sift', 'Polyphen', 'Condel']) 
                for variant in variants:
                    # print 'variant', variant.index
                    writer.writerow([variant.individual, variant.index, variant.pos_index, variant.chr, variant.pos, variant.variant_id, variant.ref, variant.alt, variant.qual, variant.filter, json.loads(variant.info), variant.format, variant.genotype_col, variant.genotype, variant.father, variant.mother, variant.read_depth, variant.gene, variant.mutation_type, variant.vartype, variant.genomes1k_maf, variant.dbsnp_maf, variant.esp_maf, variant.dbsnp_build, variant.sift, variant.sift_pred, variant.polyphen2, variant.polyphen2_pred, variant.condel, variant.condel_pred, variant.dann, variant.cadd, variant.is_at_omim, variant.is_at_hgmd, variant.hgmd_entries, variant.snpeff_effect, variant.snpeff_impact, variant.snpeff_func_class, variant.snpeff_codon_change, variant.snpeff_aa_change, variant.snpeff_gene_name, variant.snpeff_biotype, variant.snpeff_gene_coding, variant.snpeff_transcript_id, variant.snpeff_exon_rank, variant.vep_allele, variant.vep_gene, variant.vep_feature, variant.vep_feature_type, variant.vep_consequence, variant.vep_cdna_position, variant.vep_cds_position, variant.vep_protein_position, variant.vep_amino_acids, variant.vep_codons, variant.vep_existing_variation, variant.vep_distance, variant.vep_strand, variant.vep_symbol, variant.vep_symbol_source, variant.vep_sift, variant.vep_polyphen, variant.vep_condel])
                return response
            #summary
            summary['genes'] = variants.values_list('gene', flat=True)
            summary['genes'] = sorted(list(set(summary['genes'])))
            summary['n_genes'] =  len(summary['genes'])
            summary['has_variants'] = True
            summary['n_variants'] = len(variants)

            genes = get_genes(summary)            

            paginator = Paginator(variants, 100) # Show 25 contacts per page
            try:
               page = int(request.GET.get('page', '1'))
            except ValueError:
               page = 1
            try:
               variants = paginator.page(page)
            except PageNotAnInteger:
               # If page is not an integer, deliver first page.
               variants = paginator.page(1)
            except EmptyPage:
               # If page is out of range (e.g. 9999), deliver last page of results.
               variants = paginator.page(paginator.num_pages)
    #first entrance in methods
    else:
        variants = []
        summary = {}
        genes = {}

        summary['has_variants'] = False
        #fake number just not to open accordion on view 
        summary['n_genes'] = 1000
        
        genes['genes'] = []
        genes['genes_hgmd'] = []
        genes['genes_omim'] = []
        genes['genes_cgd'] = []
        form = FamilyAnalysisForm(request.user)

    return render(request,'filter_analysis/family_analysis.html',
        {'variants':variants, 
        'form':form, 
        'summary':summary,
        'query_string':query_string, 
        'filteranalysis':filteranalysis, 
        'filterconfigs':filterconfigs, 
        'genes':genes['genes'], 
        'genes_hgmd':genes['genes_hgmd'],
        'genes_omim':genes['genes_omim'],
        'genes_cgd':genes['genes_cgd']})




def wizard(request):
    form = FilterWizard([FilterWiZardForm1, FilterWiZardForm2, FilterWiZardForm3])
    if request.method == 'GET':
        print('CHECK HERE')
        query_string = request.META['QUERY_STRING']
        if query_string != '':
            print("LIMPANDO")
            new_query_string = []
            query_string = query_string.split('&')
            for item in query_string:
                if not (item.startswith('csrfmiddlewaretoken') or item.startswith('hash') or item.startswith('wizard')):
                    #get here only the ones need to be cleaned Ex. 1-chr
                    item = "-".join(item.split('-', 2)[1:])
                    new_query_string.append(item)

            #create new query
            filterstring = "&".join(new_query_string)
            # return HttpResponseRedirect('/filter_analysis/?%s' % (filterstring))
            return redirect(reverse('filter_analysis')+'?'+filterstring)
                    
                    
                     
                
                
    return form(context=RequestContext(request), request=request)


class FilterAnalysisUpdateView(UpdateView):
    model = FilterAnalysis    
    def get_success_url(self):
        return reverse('filter_analysis')

class FilterAnalysisDeleteView(DeleteView):
    model = FilterAnalysis    
    def get_success_url(self):
        return reverse('filter_analysis')

class FilterConfigUpdateView(UpdateView):
    model = FilterConfig
    template_name = "filter_analysis/filteranalysis_form.html"    
    def get_success_url(self):
        return reverse('filter_analysis')

class FilterConfigDeleteView(DeleteView):
    model = FilterConfig    
    template_name = "filter_analysis/filteranalysis_confirm_delete.html"
    def get_success_url(self):
        return reverse('filter_analysis')


def create(request):
    print('Hello')
    filterstring = request.META['QUERY_STRING']
    print(filterstring)
    if request.method == 'POST':
        form = Filter(request.POST)        
        if form.is_valid():
            #use id for unique names
            filter = FilterAnalysis.objects.create(user=request.user)
            filter.name = request.POST['name']
            filter.filterstring = form.cleaned_data['filterstring']
            filter.save()
            #return HttpResponseRedirect('/filter_analysis/?%s' % (filter.filterstring))
            return redirect(reverse('filter_analysis')+'?'+filter.filterstring)
    else:
        form = Filter(initial={'filterstring': filterstring})
        
    return render(request, 'filter_analysis/createfilter.html', {'form': form})


def family_analysis_create_filter(request):
    print('Hello')
    filterstring = request.META['QUERY_STRING']
    print(filterstring)
    if request.method == 'POST':
        form = FamilyFilter(request.POST)        
        if form.is_valid():
            #use id for unique names
            filter = FamilyFilterAnalysis.objects.create(user=request.user)
            filter.name = request.POST['name']
            filter.filterstring = form.cleaned_data['filterstring']
            filter.save()
            #return HttpResponseRedirect('/filter_analysis/family_analysis/?%s' % (filter.filterstring))
            return redirect(reverse('family_analysis')+'?'+filter.filterstring)
            # return redirect('mendelmd/%s' % (reverse('family_analysis')+'?'+filter.filterstring))
    else:
        form = FamilyFilter(initial={'filterstring': filterstring})
        
    return render(request, 'filter_analysis/createfilter.html', {'form': form})


def createconfig(request):
    print('Hello Config')
    query_string = request.META['QUERY_STRING']
    new_query_string = []
    for item in query_string.split('&'):
        if not item.startswith('individuals'):
             new_query_string.append(item)
    query_string = "&".join(new_query_string)
    filterstring = query_string

    if request.method == 'POST':
        form = Filter(request.POST)        
        if form.is_valid():
            #use id for unique names
            filterconfig = FilterConfig.objects.create(user=request.user)
            filterconfig.name = request.POST['name']
            filterconfig.filterstring = form.cleaned_data['filterstring']
            filterconfig.save()
            #return HttpResponseRedirect('/filter_analysis/?%s' % (filterconfig.filterstring))
            return redirect(reverse('filter_analysis')+'?'+filterconfig.filterstring)
    else:
        form = Filter(initial={'filterstring': filterstring})
        
    return render(request, 'filter_analysis/createfilter.html', {'form': form})


