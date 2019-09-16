from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Min, Max
from django.core import serializers
from django.views.generic import UpdateView, DeleteView
from django.core.urlresolvers import reverse

#from django.contrib.formtools.wizard import FormWizard
from django.contrib.formtools.wizard.views import SessionWizardView

from .forms import FilterWiZardForm1, FilterWiZardForm2, FilterWiZardForm3, FamilyAnalysisForm
from datetime import datetime
import operator
from django.conf import settings
from .forms import *
import csv

from individuals.models import *
from filter_analysis.forms import *
from filter_analysis.models import *
from genes.models import GeneGroup, Gene, CGDEntry, GeneList

from .filter_options import *

from diseases.models import Disease, HGMDGene, HGMDPhenotype
from diseases.models import Gene as GeneDisease



import django_tables2 as tables
from django_tables2 import RequestConfig

#This is the most important function
@login_required
def family_analysis(request):
    query = {}
    exclude = {}
    summary = {}
    args = []
    query_string = request.META['QUERY_STRING']
    new_query_string = []
    for item in query_string.split('&'):
        if not item.startswith('page'):
             new_query_string.append(item)
    query_string = "&".join(new_query_string)
    
    print('query string')
    print(query_string) 
    filteranalysis = FilterAnalysis.objects.all().prefetch_related('user')
    filterconfigs = FilterConfig.objects.all().prefetch_related('user')
    if query_string != [''] and query_string != '' :
        if request.method == 'GET':
            
            form = FilterAnalysisForm(request.GET)
            
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
                order_by = 'gene_name'

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
            filter_by_hi_score(request, args)
            #SIFT
            filter_by_sift(request, args)
            #POLYPHEN
            filter_by_pp2(request, args)
            filter_by_segdup(request, args)
            #filter by disease databases
            filter_omim(request, args)
            filter_cgd(request, args)
            filter_hgmd(request, args)
            filter_genelists(request, query, args, exclude)
            #DBSNP Build
            filter_dbsnp_build(request, query)            
            #Read Depth
            filter_read_depth(request, args)            
            filter_qual(request, args)
            filter_filter(request, query)
            #Functional class
            filter_func_class(request, query)
            #IMPACT
            filter_impact(request, query)

            #exclude individuals
            exclude_individuals = request.GET.getlist('exclude_individuals')
#            print exclude_individuals
            
            #exclude groups append to individuals
            exclude_groups = request.GET.getlist('exclude_groups')
#            print exclude_groups
            exclude_individuals_list = []
            if len(exclude_groups) > 0:
                for group_id in exclude_groups:
                    group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
                    for individual in group_individuals:
                         exclude_individuals_list.append(str(str(individual)))
#                    print exclude_individuals_list
                    
            exclude_individuals_list = exclude_individuals_list + exclude_individuals
#            print exclude_individuals_list
            exclude_individuals_variants = {}
            #exclude variants from individuals
            if len(exclude_individuals_list) > 0:
                
                #for all individuals in exclude list
                for individual in exclude_individuals_list:
                    individual_variants = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values('chromossome', 'pos', 'genotype')
                    for variant in individual_variants:
                        id = '%s-%s' % (variant['chromossome'], variant['pos'])                        
                        if id in exclude_individuals_variants:
                            exclude_individuals_variants[id][variant['genotype']] = 0
                        else:
                            exclude_individuals_variants[id] = {}
                            exclude_individuals_variants[id][variant['genotype']] = 0
                            
            #INDIVIDUALS (MUST BE THE LAST ONE...) WHY ???
            individuals = request.GET.getlist('individuals')
            
            groups = request.GET.getlist('groups')
            print(groups)
            individuals_list = []
            if len(groups) > 0:
                for group_id in groups:
                    group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
                    for individual in group_individuals:
                         individuals_list.append(str(str(individual)))
                    print(individuals_list)
                    
            individuals_list = individuals_list + individuals
#            print 'Hello World Raony'
            if len(individuals_list) > 0:
                query['individual_id__in'] = individuals_list
                #exclude variants from individuals_list
                if len(exclude_individuals_list) > 0:
    #                print 'now excluding variants from exclude_individuals'
                    variants_ids = []
                    #get variants from all select individuals    
                    variants = Variant.objects.filter(*args, **query).exclude(**exclude).values('id', 'chromossome', 'pos', 'genotype')
                    for variant in variants:
                        id = '%s-%s' % (variant['chromossome'], variant['pos'])
                        if id in exclude_individuals_variants:
                            if not variant['genotype'] in exclude_individuals_variants[id]:
                                variants_ids.append(variant['id'])
                        else:
                            variants_ids.append(variant['id'])
    #                print len(variants_ids)
                    query['pk__in'] = variants_ids
                
                
                # OPTION variants per gene
                variants_per_gene = request.GET.get('variants_per_gene')
                #option GENES in COMMON
                genes_in_common = request.GET.get('genes_in_common', '')
                
                print('variants per gene')
                print(variants_per_gene)
                if variants_per_gene != '':
                    
                    variants_per_gene = int(variants_per_gene)
    #                print 'Variants per gene'
                    variants_per_gene_option = request.GET.get('variants_per_gene_option', '')
                    
                    print('Debugging')
                    print(variants_per_gene)
                    print(variants_per_gene_option)
                    genes_exclude_list = []
                    genes_only_list = []
                    #this works for 2 indivuduals in list and with show only genes with variants in both option on
                    for individual in individuals_list:
#                        print individual
#                        print query
#                        print exclude
                        print('get list of all genes for each individual')
                        individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values('gene_name').exclude(gene_name="").annotate(count=Count('gene_name')).distinct() #.aggregate(Count('gene_name', distinct=True))
                        print(len(individual_genes))
    #                    print len(individual_genes)
                        if variants_per_gene_option == '>':    
                            for gene in individual_genes:
                                if gene['count'] >= variants_per_gene:
                                    genes_only_list.append(gene['gene_name'])
                                else:
                                    if genes_in_common == 'on':
                                        genes_exclude_list.append(gene['gene_name'])
                                        
                        elif variants_per_gene_option == '<':                    
                            for gene in individual_genes:
                                if gene['count'] <= variants_per_gene:
                                    genes_only_list.append(gene['gene_name'])
                                else:
                                    if genes_in_common == 'on':
                                        genes_exclude_list.append(gene['gene_name'])
                        elif variants_per_gene_option == '=':
                            for gene in individual_genes:
                                if gene['count'] == variants_per_gene:
                                    genes_only_list.append(gene['gene_name'])
                                else:
                                    if genes_in_common == 'on':
                                        genes_exclude_list.append(gene['gene_name'])
                    #remove variants without gene name                    
                    args.append(Q(gene_name__in=genes_only_list))
                    args.append(~Q(gene_name__in=genes_exclude_list))
                
                if genes_in_common == 'on':
                    #get all genes from individual
                    individual_gene_list = []
                    for individual in individuals_list:
                        individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values_list('gene_name', flat=True).exclude(gene_name="").distinct()
                        individual_genes = set(list(individual_genes))
                        individual_gene_list.append(individual_genes)
                    genes_in_common_list = set.intersection(*individual_gene_list)                    
                    query['gene_name__in'] = genes_in_common_list#genes_in_common_list

                
                positions_in_common = request.GET.get('positions_in_common', '')
                if positions_in_common == 'on':
                    #get all genes from individual
                    individual_positions_list = []
                    for individual in individuals_list:
                        #should be done with an index ex. 1-2835763-C-T
                        individual_positions = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values_list('pos', flat=True).distinct()
                        individual_positions = set(list(individual_positions))
                        individual_positions_list.append(individual_positions)
                    positions_in_common_list = set.intersection(*individual_positions_list)                    
                    query['pos__in'] = positions_in_common_list#genes_in_common_list
            
            #last call to the DATABASE Finally!!!!!! 
            variants = Variant.objects.filter(*args, **query).exclude(**exclude).prefetch_related('individual').order_by(order_by)
            #export to csv
            export = request.GET.get('export', '')
            if export != '':
                if export == 'csv':
                    response = HttpResponse(mimetype='text/csv')
                    response['Content-Disposition'] = 'attachment; filename=export.csv'
                    writer = csv.writer(response)
                    
                elif export == 'txt':
                    response = HttpResponse(mimetype='text/plain')
                    response['Content-Disposition'] = 'attachment; filename=export.txt'
                    writer = csv.writer(response, delimiter='\t', quoting=csv.QUOTE_NONE)    
                writer.writerow(['Individual',
                'Chromossome', 'Variant Id', 'Pos', 'Qual', 'Ref', 'Alt', 'Genotype',
                'Genotype Info', 'Read Depth', 'Snpe Eff', 'Functional Class', 'Gene',
                'Impact', 'Variant is Clinical', '100Genomes Frequency', 'dbSNP135 Frequency',
                'ESP5400 Frequency', 'ESP5400 EA/AA/ALL', 'ESP5400 Total Allele Count',
                'SIFT', 'Polyphen2', 'dbSNP Build', 'Amino Acid Change',
                'Cdna Position', 'Granthamscore', 'Protein Position']) 
                for variant in variants:
                    writer.writerow([variant.individual, variant.chromossome,
                    variant.variant_id, variant.pos, variant.qual, variant.ref,
                    variant.alt, variant.genotype, variant.genotype_info,
                    variant.read_depth, variant.snp_eff,
                    variant.snp_eff_functional_class, variant.gene_name, variant.impact,
                    variant.dbsnp_pm, variant.genomes1k_maf, variant.dbsnp_gmaf,
                    variant.esp_maf_total, variant.ann_esp_maf, variant.tac,
                    variant.sift, variant.polyphen, variant.dbsnp_build,
                    variant.amino_acid_change, variant.cdna_position,
                    variant.granthamscore, variant.protein_position])
                return response

            summary['genes'] = variants.values_list('gene_name', flat=True)
            summary['genes'] = sorted(list(set(summary['genes'])))
            summary['n_genes'] =  len(summary['genes'])
            summary['has_variants'] = True
            
            if summary['n_genes'] < 500:
                genes = Gene.objects.filter(symbol__in=list(summary['genes'])).values('symbol', 'diseases').prefetch_related('diseases')                
                genes_hgmd = HGMDGene.objects.filter(symbol__in=list(summary['genes'])).prefetch_related('diseases')# | reduce(lambda x, y: x | y, [Q(aliases__icontains=word) for word in list(summary['genes'])]))
                #return Disease.objects.filter(Q(name__icontains=name)|Q(gene_names__icontains=name))
                #for each gene name create a query
                queries = [Q(gene_names__icontains=value) for value in list(summary['genes'])]
                if len(queries) > 0:
                    query = queries.pop()
                    for item in queries:
                        query |= item
                    genes_omim = GeneDisease.objects.filter(official_name__in=list(summary['genes'])).prefetch_related('diseases')#query
                else:
                    genes_omim = []
                #get genes at CGD
                genes_cgd = CGDEntry.objects.filter(GENE__in=list(summary['genes'])).prefetch_related('CONDITIONS')

            else:
                genes = []
                genes_hgmd = []
                genes_omim = []
                genes_cgd = []

            summary['n_variants'] = len(variants)
            paginator = Paginator(variants, 25) # Show 25 contacts per page
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
        summary['has_variants'] = False
        #fake number just not to open accordion on view 
        summary['n_genes'] = 1000
        genes = []
        genes_hgmd = []
        genes_omim = []
        genes_cgd = []
        
        form = FilterAnalysisForm()                    
    return render(request, 'filter_analysis/index.html', 
        {'variants':variants, 
        'form':form, 
        'summary':summary, 
        'query_string':query_string, 
        'filteranalysis':filteranalysis, 
        'filterconfigs':filterconfigs, 
        'genes':genes, 
        'genes_hgmd':genes_hgmd,
        'genes_omim':genes_omim,
        'genes_cgd':genes_cgd})



@login_required
def oldfamily_analysis(request):
    query = {}
    exclude = {}
    summary = {}
    args = []
    query_string = request.META['QUERY_STRING']
    new_query_string = []
    #this is to remove page from query
    for item in query_string.split('&'):
        if not item.startswith('page'):
             new_query_string.append(item)
    query_string = "&".join(new_query_string)
    
    print('query string')
    print(query_string) 
    #retrieve saved filter_analysis and config
    filteranalysis = FamilyFilterAnalysis.objects.all()
    filterconfigs = FilterConfig.objects.all()

    if query_string != [''] and query_string != '' :
        if request.method == 'GET':
            request.GET = request.GET.copy()
            form = FamilyAnalysisForm(request.GET)
            
            inheritance_option = request.GET.get('inheritance_option', '')
            remove_not_in_parents = request.GET.get('remove_not_in_parents', '')
            remove_in_both_parents = request.GET.get('remove_in_both_parents', '')

#            
            filter_inheritance_option(request)
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
            filter_by_hi_score(request, args)
            #SIFT
            filter_by_sift(request, args)
            #POLYPHEN
            filter_by_pp2(request, args)
            filter_by_segdup(request, args)
            #filter by disease databases
            filter_omim(request, args)
            filter_cgd(request, args)
            filter_hgmd(request, args)
            filter_genelists(request, query, args, exclude)
            #DBSNP Build
            filter_dbsnp_build(request, query)            
            #Read Depth
            filter_read_depth(request, args)            
            filter_qual(request, args)
            filter_filter(request, query)
            #Functional class
            filter_func_class(request, query)
            #IMPACT
            filter_impact(request, query)

            

            # Build Family Variants dict
            print('Get family variants')
            father = request.GET.get('father', '')
            mother = request.GET.get('mother', '')
            children = request.GET.getlist('children')

            parents_variants = {'father':{}, 'mother':{}}
            parents = {'father':father, 'mother':mother}
            #for each parent get variants from parents and build dict for future filtering
            for individual in parents:
                query['individual_id__in'] = [parents[individual]]
                print(query)
                individual_variants = Variant.objects.filter(*args, **query).values('chromossome', 'pos', 'genotype', 'gene_name')
                print('individual variants')
                print(individual, parents[individual])
                print(len(individual_variants)) #all right
                for variant in individual_variants:
                    id = '%s-%s' % (variant['chromossome'], variant['pos'])
                    gene = variant['gene_name']
                    #check if gene don't exists in structure first time of gene in structure 
                    if gene not in parents_variants[individual]:
                        parents_variants[individual][gene] = {}
                    parents_variants[individual][gene][id] = {}
                    parents_variants[individual][gene][id][variant['genotype']] = 0
                            
            #add father and mother to list of exclude individuals                
            filter_inheritance_option_exclude_individuals(request)
            #exclude individuals
            exclude_individuals = request.GET.getlist('exclude_individuals')
            
            print('exclude individuals %s' % exclude_individuals)
            
            #exclude groups append to individuals
            exclude_groups = request.GET.getlist('exclude_groups')
            print(exclude_groups)
            exclude_individuals_list = []
            if len(exclude_groups) > 0:
                for group_id in exclude_groups:
                    group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
                    for individual in group_individuals:
                         exclude_individuals_list.append(str(str(individual)))
#                    print exclude_individuals_list
                    
            exclude_individuals_list = exclude_individuals_list + exclude_individuals
            print(exclude_individuals_list)
            exclude_individuals_variants = {}
            
            print('#exclude variants from individuals')
            if len(exclude_individuals_list) > 0:
                #for all individuals in exclude list get variants and create list for exclusion with genotypes in python
                for individual in exclude_individuals_list:
                    query['individual_id__in'] = [individual]
                    print(query)
                    
                    individual_variants = Variant.objects.filter(*args, **query).exclude(**exclude).values('chromossome', 'pos', 'genotype')
                    print(len(individual_variants))
                    for variant in individual_variants:
                        id = '%s-%s' % (variant['chromossome'], variant['pos'])                        
                        if id in exclude_individuals_variants:
                            exclude_individuals_variants[id][variant['genotype']] = 0
                        else:
                            exclude_individuals_variants[id] = {}
                            exclude_individuals_variants[id][variant['genotype']] = 0
            
            
            #set mutation type for trio_option
            filter_mutation_type(request, args)
            filter_inheritance_option_mutation_type(request, args)
            
            
            
            #Fill Groups
            individuals = request.GET.getlist('individuals')
            groups = request.GET.getlist('groups')
            # print groups
            individuals_list = []
            if len(groups) > 0:
                for group_id in groups:
                    group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
                    for individual in group_individuals:
                         individuals_list.append(str(str(individual)))
                    print(individuals_list)
                    
            individuals_list = individuals_list + individuals
            
            # child = request.GET.get('child', '')
            if len(children) > 0:
                for child in children:
                    individuals_list.append(child)


            #apply some rules based on inheritance model and remove_not seeing in parents
            #after fill dicts with ids apply some rules for filtering
                

            #final query getting the variants to show
            query['individual_id__in'] = individuals_list
            variants = Variant.objects.filter(*args, **query).exclude(**exclude).order_by('gene_name')
            print(len(variants))
            #this function serves to create a list of exclude_gene_list exclude_variant_list based on inheritance and
            # remove not in parents options
            
            #recessive inheritance
            if inheritance_option == '1':
                print('Usando modelo recessivo')
                if remove_not_in_parents == 'on':
                    print('remove not seing in parents')
                    children_dict = {}
                    for child in children:
                        print('child %s' % (child))
                        children_dict[child] = {}
                        print(len(variants))
                        for variant in variants:
                            # print '%s vs %s' % (variant.individual.id, child)
                            if str(variant.individual.id) == str(child):
                                print('variant == child')
                                id = '%s-%s' % (variant.chromossome, variant.pos)
                                gene = variant.gene_name
                                #check if gene don't exists in structure first time of gene in structure 
                                if gene not in children_dict[child]:
                                    children_dict[child][gene] = {}
                                if id not in children_dict[child][gene]:
                                    children_dict[child][gene][id] = {}
                                children_dict[child][gene][id][variant.genotype] = variant.id
                                children_dict[child][gene][id]['id'] = variant.id
                    #now search for recessive excluding variants not present in both parents
                    exclude_gene_list =[]
                    exclude_variant_list=[]
                    #for every child
                    for child in children:
                        #for every gene in every child
                        for gene in children_dict[child]:
                            #check if gene is present in both parents
                            if gene in parents_variants['father'] and gene in parents_variants['mother']:
                                for id in children_dict[child][gene]:
                                    #check if id is present in both parents
                                    if (id in parents_variants['father'][gene]) and (id in parents_variants['mother'][gene]):
                                        if '1/1' in parents_variants['mother'][gene][id] or '1/1' in parents_variants['mother'][gene][id]:
                                            exclude_variant_list.append(list(children_dict[child][gene][id].values())[0])
                                    else:
                                        exclude_variant_list.append(list(children_dict[child][gene][id].values())[0])
                            #if not add gene to exclude gene list
                            else:
                                exclude_gene_list.append(gene)
                    print(len(exclude_gene_list))

                    if 'gene_name__in' in exclude:
                        exclude['gene_name__in'] = exclude['gene_name__in']+exclude_gene_list
                    else:
                        exclude['gene_name__in'] = exclude_gene_list
                    
                    args.append(~Q(id__in=exclude_variant_list))
                    variants = Variant.objects.filter(*args, **query).exclude(**exclude).order_by('gene_name')
                    print(len(variants))




            #compound heterozygous
            if inheritance_option == '3':
                print('doing compound heterozygous')
                #build children dict with genes and variants
                children_dict = {}
                for child in children:
                    children_dict[child] = {}
                    # print 'child %s' % children
                    for variant in variants:
                        if str(variant.individual.id) == str(child):
                            id = '%s-%s' % (variant.chromossome, variant.pos)
                            gene = variant.gene_name
                            #check if gene don't exists in structure first time of gene in structure 
                            if gene not in children_dict[child]:
                                children_dict[child][gene] = {}
                            if id not in children_dict[child][gene]:
                                children_dict[child][gene][id] = {}
                            children_dict[child][gene][id][variant.genotype] = variant.id
                            children_dict[child][gene][id]['id'] = variant.id

                #finished building child dict
                # print 'checking if verything is ok with child dict'
                # print children_dict['6']['KIF14']
                # print children_dict['7']['KIF14']

                #now search for compound heterozygous magic happens in here!
                exclude_gene_list =[]
                exclude_variant_list=[]
                # print 'opps erro no children'
                # print children
                for child in children:
                    #for every gene
                    for gene in children_dict[child]:
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
                            #     print children_dict[child][gene]
                            #     print parents_variants['father'][gene]
                            #     print parents_variants['mother'][gene]
                            #for every variant in child gene
                            for id in children_dict[child][gene]:

                                if (id in parents_variants['father'][gene]) and (id not in parents_variants['mother'][gene]):
                                    if '1/1' not in parents_variants['father'][gene][id]:
                                        one_comes_only_from_father = True
                                if (id in parents_variants['mother'][gene]) and (id not in parents_variants['father'][gene]):
                                    if '1/1' not in parents_variants['mother'][gene][id]:
                                        one_comes_only_from_mother = True
                                if id in parents_variants['mother'][gene]:
                                    if '1/1' in parents_variants['mother'][gene][id]:
                                        exclude_variant_list.append(list(children_dict[child][gene][id].values())[0])
                                if id in parents_variants['father'][gene]:
                                    if '1/1' in parents_variants['father'][gene][id]:
                                        exclude_variant_list.append(list(children_dict[child][gene][id].values())[0])
                                #if present in both exclude variants
                                if remove_in_both_parents == 'on':
                                    if (id in parents_variants['father'][gene]) and (id in parents_variants['mother'][gene]):
                                        exclude_variant_list.append(list(children_dict[child][gene][id].values())[0])

                                #if id not seeing in both parents remove from results
                                if remove_not_in_parents== 'on':
                                    if id not in parents_variants['mother'][gene]:
                                        if id not in parents_variants['father'][gene]:
                                            # print 'Exclui variant %s' % (id)
                                            exclude_variant_list.append(list(children_dict[child][gene][id].values())[0])
                            if one_comes_only_from_father and one_comes_only_from_mother:
                                pass
                            else:
                                exclude_gene_list.append(gene)
                        #option for removing variants from genes not seing in parents
                        else:
                            if remove_not_in_parents == 'on':
                                exclude_gene_list.append(gene)
                        
                print(len(exclude_gene_list))
                if 'gene_name__in' in exclude:
                    exclude['gene_name__in'] = exclude['gene_name__in']+exclude_gene_list
                else:
                    exclude['gene_name__in'] = exclude_gene_list
                
                args.append(~Q(id__in=exclude_variant_list))
#                print exclude['id__in']
                variants = Variant.objects.filter(*args, **query).exclude(**exclude).order_by('gene_name')
                print(len(variants))
                #Compound heterozygous ends in here



            #INDIVIDUALS (MUST BE THE LAST ONE...) WHY ??? Cause it's the most important!            
            #getting variants from all individuals selected THIS MUST BE THE LAST ONE
            if len(individuals_list) > 0:
                query['individual_id__in'] = individuals_list
                #exclude variants from individuals_list
                if len(exclude_individuals_list) > 0:
    #               print 'now excluding variants from exclude_individuals'
                    variants_ids = []
                    #get variants from all select individuals    
                    variants = Variant.objects.filter(*args, **query).exclude(**exclude).values('id', 'chromossome', 'pos', 'genotype')
    #               print 'variants from selected individuals'
    #               print variants.count() 
                    #create index in python for searching individuals variants that wont be excluded 
                    for variant in variants:
                        id = '%s-%s' % (variant['chromossome'], variant['pos'])
                        if id in exclude_individuals_variants:
                            if not variant['genotype'] in exclude_individuals_variants[id]:
                                #let only denovo variants pass  #ugly hack removing 0/0 and 1/1 variants seeing in parents
                                if inheritance_option == '2':
                                    if '1/1' not in exclude_individuals_variants[id]:
                                        if '0/1' not in exclude_individuals_variants[id]:
                                            variants_ids.append(variant['id'])
                                elif inheritance_option == '3':
                                    if '1/1' not in exclude_individuals_variants[id]:
                                        variants_ids.append(variant['id'])
                                else:
                                    variants_ids.append(variant['id'])
                        else:
                            variants_ids.append(variant['id'])
    #                print len(variants_ids)
                    query['pk__in'] = variants_ids
                
                # OPTION variants per gene
                #exclude all genes that doesn't match this criteria Ex. >= 2 variants per gene
                variants_per_gene = request.GET.get('variants_per_gene')
                print('variants per gene')
                print(variants_per_gene)
                if variants_per_gene != '':
                    
                    variants_per_gene = int(variants_per_gene)
                    print('Variants per gene')
                    variants_per_gene_option = request.GET.get('variants_per_gene_option', '')
                    genes_exclude_list = []
                    for individual in individuals_list:
    #                    print individual
                        individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values('gene_name').exclude(gene_name="").annotate(count=Count('gene_name')).distinct() #.aggregate(Count('gene_name', distinct=True))
                        print(len(individual_genes))
                        print('len individual genes')
                        if variants_per_gene_option == '>':    
                            for gene in individual_genes:
                                if gene['count'] < variants_per_gene:
                                    genes_exclude_list.append(gene['gene_name'])
                        elif variants_per_gene_option == '<':                    
                            for gene in individual_genes:
                                if gene['count'] > variants_per_gene:
                                    genes_exclude_list.append(gene['gene_name'])
                        elif variants_per_gene_option == '=':
                            for gene in individual_genes:
                                if gene['count'] != variants_per_gene:
                                    genes_exclude_list.append(gene['gene_name'])
                    #remove variants without gene name
                    genes_exclude_list.append('')
                    
                    if 'gene_name__in' in exclude:
                        exclude['gene_name__in'] = exclude['gene_name__in'] + genes_exclude_list
                    else:
                        exclude['gene_name__in'] = genes_exclude_list
                    
                #option GENES in COMMON
                genes_in_common = request.GET.get('genes_in_common', '')
                if genes_in_common == 'on':
                    
                    #get all genes from individual
                    individual_gene_list = []
                    for individual in individuals_list:
    #                    print individual
                        individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values_list('gene_name', flat=True).exclude(gene_name="").distinct()
                        individual_genes = set(list(individual_genes))
                        individual_gene_list.append(individual_genes)

                    genes_in_common_list = set.intersection(*individual_gene_list)                    
                    query['gene_name__in'] = genes_in_common_list#genes_in_common_list
                

        
#             #after fill dicts with ids apply some rules for filtering
                

#             #final query getting the variants to show
#             query['individual_id__in'] = individuals_list
            variants = Variant.objects.filter(*args, **query).exclude(**exclude).order_by('gene_name', 'individual')
            print(len(variants))
            #final after treating all variants
            #just for visual stuff - seing father mother genotypes
            for variant in variants:
                id = '%s-%s' % (variant.chromossome, variant.pos)
                gene = variant.gene_name
                if gene in  parents_variants['father']:
                    if id in parents_variants['father'][gene]:
                        variant.father =  list(parents_variants['father'][gene][id].keys())[0]
                if gene in  parents_variants['mother']:
                    if id in parents_variants['mother'][gene]:
                        variant.mother =  list(parents_variants['mother'][gene][id].keys())[0]
                #check recessive

            summary['n_variants'] = variants.count()
            summary['n_genes'] = variants.values('gene_name').exclude(gene_name="").distinct().count()
            summary['genes'] = variants.values_list('gene_name', flat=True).exclude(gene_name="").distinct()
            summary['genes'] = sorted(list(set(summary['genes'])))
            # summary['genes'] = variants.values('gene_name').exclude(gene_name="").distinct()

            print('summary genes')
            print(summary['genes'])
            
#            if summary['n_genes'] < 1000:
#                summary['genes'] = variants.values('gene_name').exclude(gene_name="").distinct()
#            else:
#                summary['genes'] = ""
                
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
            
                         
            form = FamilyAnalysisForm(request.GET)
    
    #first entrance in methods
    else:
        variants = []
        summary = []
        form = FamilyAnalysisForm()            
    #export to csv
    export = request.GET.get('export', '')
    if export != '':
        variants = Variant.objects.filter(*args, **query).exclude(**exclude).order_by('gene_name')
    
        
        if export == 'csv':
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Variants_from_Mendel_MD.csv'
            writer = csv.writer(response)
            
        elif export == 'txt':
            response = HttpResponse(mimetype='text/plain')
            response['Content-Disposition'] = 'attachment; filename=Variants_from_Mendel_MD.txt'
            writer = csv.writer(response, delimiter='\t', quoting=csv.QUOTE_NONE)
        
        writer.writerow(['Individual',
        'Chromossome', 'Variant Id', 'Pos', 'Qual', 'Ref', 'Alt', 'Genotype',
        'Genotype Info', 'Read Depth', 'Snpe Eff', 'Functional Class', 'Gene',
        'Impact', 'Variant is Clinical', '100Genomes Frequency', 'dbSNP135 Frequency',
        'ESP5400 Frequency', 'ESP5400 EA/AA/ALL', 'ESP5400 Total Allele Count',
        'SIFT', 'Polyphen2', 'dbSNP Build', 'Amino Acid Change',
        'Cdna Position', 'Granthamscore', 'Protein Position']) 
        for variant in variants:
            writer.writerow([variant.individual, variant.chromossome,
            variant.variant_id, variant.pos, variant.qual, variant.ref,
            variant.alt, variant.genotype, variant.genotype_info,
            variant.read_depth, variant.snp_eff,
            variant.snp_eff_functional_class, variant.gene_name, variant.impact,
            variant.dbsnp_pm, variant.genomes1k_maf, variant.dbsnp_gmaf,
            variant.esp_maf_total, variant.ann_esp_maf, variant.tac,
            variant.sift, variant.polyphen, variant.dbsnp_build,
            variant.amino_acid_change, variant.cdna_position,
            variant.granthamscore, variant.protein_position])
        
        return response
    
        
                
    diseases = Disease.objects.distinct().order_by('name')[:5]
#    diseases = Disease.objects.a().order_by('name')[:5]
    diseases = serializers.serialize("json", diseases)

        
    return render(request, 'filter_analysis/family_analysis.html', {'variants':variants, 'form':form, 'summary':summary, 'query_string':query_string, 'diseases':diseases, 'filteranalysis':filteranalysis, 'filterconfigs':filterconfigs})

    

class FilterWizard(SessionWizardView):
    def get_template(self, step):
        if step == 0:
            return 'forms/step0.html'
        if step == 1:
            return 'forms/step1.html'
        if step == 2:
            return 'forms/step2.html'

@login_required
def oneclick(request):
    form = FilterAnalysisForm()
    if request.method == 'GET':
        print('Entrando no GET')
        # print request.META
        query_string = request.META['QUERY_STRING']
        print(query_string)
        if query_string != '':
            print("LIMPANDO")
            new_query_string = []
            query_string = query_string.split('&')
            for item in query_string:
                if not (item.startswith('csrfmiddlewaretoken') or item.startswith('hash') or item.startswith('wizard')):
                    #get here only the ones need to be cleaned Ex. 1-chr
                    #item = "-".join(item.split('-', 2)[1:])
                    new_query_string.append(item)

            #create new query
            filterstring = "&".join(new_query_string)
            # return HttpResponseRedirect('/filter_analysis/?%s' % (filterstring))
            return redirect(reverse('filter_analysis')+'?'+filterstring)

    return render(request, 'filter_analysis/oneclick.html', {'form':form})

        
@login_required
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

@login_required
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


@login_required
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


@login_required
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