from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from forms import PathwayAnalysisForm
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Min, Max
import csv
from django.contrib import messages
from django.core import serializers
from django.core.urlresolvers import reverse 

from django.views.generic import UpdateView, DeleteView

from django.shortcuts import render_to_response
#from django.contrib.formtools.wizard import FormWizard
from django.contrib.formtools.wizard.views import SessionWizardView

from pathway_analysis.forms import PathwayAnalysisForm, PathAnalysisForm

from pathway_analysis.models import Pathway
from filter_analysis.models import *
from filter_analysis.forms import *


from genes.models import GeneGroup, Gene, CGDEntry, GeneList

from diseases.models import Disease, HGMDGene, HGMDPhenotype
from diseases.models import Gene as GeneDisease


#pathwya imports
from SOAPpy import WSDL
#REST
import urllib.request, urllib.error, urllib.parse


def kegg_rest_request(query):
    url = 'http://rest.kegg.jp/%s' % (query)
    print(url)
    try:
        data = urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as e:
        print("HTTP error: %d" % e.code)
    except urllib.error.URLError as e:
        print("Network error: %s" % e.reason.args[1])
    
    return data

def parse_pathways(data):
    data = data.strip().split('\n')
    pathways = {}
    for line in data:
        line = line.split('\t')
        print(line)
        line[0] = line[0].replace('path:', '').replace('hsa', '').replace('map', '')
        pathways[line[0]] = line[1]
    return pathways

def parse_genes(data):
    #get a gene http://rest.kegg.jp/get/hsa:10683
    data = data.strip().split('\n')
    genes = []
    flag = False
    for line in data:
        if not line.startswith('GENE'):
            if line[0].isupper():
                flag = False
        if line.startswith('GENE') or flag:
            if line.startswith('GENE'):
                line = line.replace('GENE        ', '')
            else:
                line = line.strip()
            
            flag =  True
            
            line = line.split()
            
            #print 'line', line

            gene = {}
            
            
            if len(line) > 1:
                gene['id'] = line[0]
                gene['symbol'] = line[1].replace(';', '')
                gene['ko'] = line[-1]
                gene['description'] = " ".join(line[2:-2])
                genes.append(gene) 
            
            
            
            
        
        
    return genes
        

def populate(request):
#    pathway = Pathway(keggid='1234', name='Raony', genes='ABGS,SAKHA,AKJSKJ')
#    pathway.save()

    Pathway.objects.all().delete()

    pathways = kegg_rest_request('list/pathway/hsa')
    pathways = parse_pathways(pathways)
    insert_list = []
    total = len(pathways)
    
    for keggid in pathways:
        print(total)
        total = total-1
        
#        print keggid, pathways[keggid]
        pathway_data = kegg_rest_request('get/hsa%s' % (keggid))
        genes = parse_genes(pathway_data)
        print('genes')
#        print genes
        gene_list = []
        for gene in genes:
            gene_list.append(gene['symbol'])
#        print gene_list
        gene_list = ",".join(gene_list)
#        print keggid, pathways[keggid], gene_list
#        pathway_name = pathway_data.split('\n')[1].replace('NAME', '')
    
        pathway = Pathway(kegg=keggid, name=pathways[keggid], genes=gene_list)
        pathway.save()

    message = 'finish filling pathway from kegg'
    messages.add_message(request, messages.INFO, message)
    return redirect('/databases/')


# Create your views here.
@login_required
def index(request):
    if request.method == 'POST':
        form = PathAnalysisForm(request.POST)
        if  form.is_valid():
            query = form.cleaned_data['search']
            print(query)
            #here is where the magic happens!
            #search in kegg
#            data = kegg_rest_request('list/pathway/hsa')
#            pathways = kegg_rest_request('find/pathway/%s' % (query))
            pathways = Pathway.objects.filter(Q(name__icontains=query))
            # print pathways
            
    else:
        form = PathAnalysisForm()
#        pathways = kegg_rest_request('list/pathway/hsa')
        pathways = Pathway.objects.all()    
    
    
    return render_to_response('pathway_analysis/index.html', {'form': form, 'pathways': pathways}, context_instance=RequestContext(request))

@login_required
def view(request, pathway_id):
    print(pathway_id)
    
#    pathway_data = kegg_rest_request('get/hsa%s' % (pathway_id))
    pathway = Pathway.objects.get(kegg=pathway_id)

     
    pathway.genes = pathway.genes.split(',')
    print(pathway.genes)
    
#    genes = parse_genes(pathway_data)
#    pathway = {}
#    pathway['name'] = pathway_data.split('\n')[1].replace('NAME', '') 
#    #get gene_ids
#    genelist = []
#    for gene in genes:
#        
#        genelist.append('hsa:%s' % gene['id'])
##        print gene['id']
#    gene_url = '+'.join(genelist)
#    url = '/conv/ncbi-geneid/%s' % (gene_url)
#    results = kegg_rest_request(url)
    #print results
    
    
    #if request.method == 'GET':
    return render_to_response('pathway_analysis/view.html', {'pathway':pathway}, context_instance=RequestContext(request))

from filter_analysis.views import filter_analysis

#This is the most important function
@login_required
def analysis(request):
    query = {}
    exclude = {}
    summary = {}
    args = []
    results = []
    
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
            
            form = PathwayAnalysisForm(request.GET)
            
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

            filter_analysis(request,query, args, exclude)

            # #CHR
            # filter_chr(request, query)
            # #pos
            # filter_pos(request, query)
            # #snp_list
            # filter_snp_list(request, query, exclude)
            # #Gene List, this is entered by hand
            # filter_gene_list(request, query, args)
            # #Inheritance_model
            # filter_mutation_type(request, args)
            # #Clinical
            # # filter_cln(request, query)
            # #Variant type SNP EFF       
            # filter_variant_type_snpeff(request, query)
            # #DBSNP
            # filter_dbsnp(request, query)
            # #1000genomes
            # filter_by_1000g(request, args)
            # #dbsnp Freq
            # filter_by_dbsnp(request, args)
            # #Exome Variation Server Freq
            # filter_by_esp(request, args)
            # #hi score
            # filter_by_hi_score(request, args)
            # #SIFT
            # filter_by_sift(request, args)
            # #POLYPHEN
            # filter_by_pp2(request, args)
            # filter_by_segdup(request, args)
            # #filter by disease databases
            # filter_omim(request, args)
            # filter_cgd(request, args)
            # filter_hgmd(request, args)
            # filter_genelists(request, query, args, exclude)
            # #DBSNP Build
            # filter_dbsnp_build(request, query)            
            # #Read Depth
            # filter_read_depth(request, args)            
            # filter_qual(request, args)
            # filter_filter(request, query)
            # #Functional class
            # filter_func_class(request, query)
            # #IMPACT
            # filter_impact(request, query)

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
                    individual_variants = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values('chr', 'pos', 'genotype')
                    for variant in individual_variants:
                        id = '%s-%s' % (variant['chr'], variant['pos'])                        
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
                    variants = Variant.objects.filter(*args, **query).exclude(**exclude).values('id', 'chr', 'pos', 'genotype')
                    for variant in variants:
                        id = '%s-%s' % (variant['chr'], variant['pos'])
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
                        individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values('gene').exclude(gene="").annotate(count=Count('gene')).distinct() #.aggregate(Count('gene', distinct=True))
                        print(len(individual_genes))
    #                    print len(individual_genes)
                        if variants_per_gene_option == '>':    
                            for gene in individual_genes:
                                if gene['count'] >= variants_per_gene:
                                    genes_only_list.append(gene['gene'])
                                else:
                                    if genes_in_common == 'on':
                                        genes_exclude_list.append(gene['gene'])
                                        
                        elif variants_per_gene_option == '<':                    
                            for gene in individual_genes:
                                if gene['count'] <= variants_per_gene:
                                    genes_only_list.append(gene['gene'])
                                else:
                                    if genes_in_common == 'on':
                                        genes_exclude_list.append(gene['gene'])
                        elif variants_per_gene_option == '=':
                            for gene in individual_genes:
                                if gene['count'] == variants_per_gene:
                                    genes_only_list.append(gene['gene'])
                                else:
                                    if genes_in_common == 'on':
                                        genes_exclude_list.append(gene['gene'])
                    #remove variants without gene name                    
                    args.append(Q(gene__in=genes_only_list))
                    args.append(~Q(gene__in=genes_exclude_list))
                
                if genes_in_common == 'on':
                    #get all genes from individual
                    individual_gene_list = []
                    for individual in individuals_list:
                        individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values_list('gene', flat=True).exclude(gene="").distinct()
                        individual_genes = set(list(individual_genes))
                        individual_gene_list.append(individual_genes)
                    genes_in_common_list = set.intersection(*individual_gene_list)                    
                    query['gene__in'] = genes_in_common_list#genes_in_common_list

                
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
                    writer.writerow([variant.individual, variant.chr,
                    variant.variant_id, variant.pos, variant.qual, variant.ref,
                    variant.alt, variant.genotype, variant.genotype_info,
                    variant.read_depth, variant.snp_eff,
                    variant.snp_eff_functional_class, variant.gene, variant.impact,
                    variant.dbsnp_pm, variant.genomes1k_maf, variant.dbsnp_gmaf,
                    variant.esp_maf_total, variant.ann_esp_maf, variant.tac,
                    variant.sift, variant.polyphen, variant.dbsnp_build,
                    variant.amino_acid_change, variant.cdna_position,
                    variant.granthamscore, variant.protein_position])
                return response

            summary['genes'] = variants.values_list('gene', flat=True)
            summary['genes'] = sorted(list(set(summary['genes'])))
            summary['n_genes'] =  len(summary['genes'])
            summary['has_variants'] = True
            
            if summary['n_genes'] < 500:
                genes = Gene.objects.filter(symbol__in=list(summary['genes'])).values('symbol', 'diseases').prefetch_related('diseases')                
                genes_hgmd = HGMDGene.objects.filter(symbol__in=list(summary['genes'])).prefetch_related('diseases')# | reduce(lambda x, y: x | y, [Q(aliases__icontains=word) for word in list(summary['genes'])]))
                #return Disease.objects.filter(Q(name__icontains=name)|Q(genes__icontains=name))
                #for each gene name create a query
                queries = [Q(genes__icontains=value) for value in list(summary['genes'])]
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

            #Do pathway analysis here
            pathways = Pathway.objects.all().order_by('name')

            for pathway in pathways:
                pathway.variants = []
                pathway.genes = pathway.genes.split(',')

            #now group variants object by pathways
            if variants != None:
                #create dict
                variants_dicts = {}
                for variant in variants:
                    for pathway in pathways:
                        if variant.gene in pathway.genes:
                            pathway.variants.append(variant)
                            if pathway not in results:
                                results.append(pathway)
                pathways = sorted(results, key=lambda k: k.name)
            else:
                pathways = []            

            # Filter option for pathways for individuals_per_pathway
            #check for each pathway if there (<=,>=,==) at least n individuals per pathway
            individuals_per_pathway = request.GET.get('individuals_per_pathway')
            not_allowed = ['', None]
            if individuals_per_pathway not in not_allowed:
                new_pathways = []
                individuals_per_pathway = int(individuals_per_pathway)
                print('Individuals per pathway')
                individuals_per_pathway_option = request.GET.get('individuals_per_pathway_option', '')
                
                for pathway in pathways:
    #                print pathway.name
                    #count individuals
                    individuals_in_pathway = []
                    
    #                print len(pathway.variants)
                    for variant in pathway.variants:
                        if variant.individual not in individuals_in_pathway:
                            individuals_in_pathway.append(variant.individual)
                            
                    #check size of individuals_in_pathway:
    #                print 'individuals_in_pathway'
                    if individuals_per_pathway_option == '>':
                        if len(individuals_in_pathway) >= individuals_per_pathway:
                            new_pathways.append(pathway)
                pathways = new_pathways




            
    #first entrance in methods
    else:
        pathways = []
        summary = {}
        summary['has_variants'] = False
        #fake number just not to open accordion on view 
        summary['n_genes'] = 1000
        genes = []
        genes_hgmd = []
        genes_omim = []
        genes_cgd = []
        
        form = PathwayAnalysisForm()                    
    return render_to_response('pathway_analysis/analysis.html', 
        {'pathways':pathways,
        'form':form, 
        'summary':summary, 
        'query_string':query_string, 
        'filteranalysis':filteranalysis, 
        'filterconfigs':filterconfigs, 
        'genes':genes, 
        'genes_hgmd':genes_hgmd,
        'genes_omim':genes_omim,
        'genes_cgd':genes_cgd}, context_instance=RequestContext(request))



@login_required
def index(request):
    args = []
    query = {}
    summary= {}
    results = []

    if request.method == 'GET':
        
        #prepare pathway form
        form = PathwayAnalysisForm(request.GET)
        
        #call method get_filtered_variants

        result = get_filtered_variants(request)

        if result:
            variants = result['variants']
            summary = result['summary']
        else:
           variants=None 
        
        #get all pathways for pathway analysis
        pathways = Pathway.objects.all().order_by('name')

        # all_genes_from_pathways = []
        # for pathway in pathways:
        #     pathway.variants = []
        #     pathway.genes = pathway.genes.split(',')
            # all_genes_from_pathways = all_genes_from_pathways + pathway.genes
        # print len(all_genes_from_pathways)


        #now group variants object by pathways
        if variants != None:
            #create dict
            variants_dicts = {}
            for variant in variants:
                for pathway in pathways:
                    if variant.gene in pathway.genes:
                        pathway.variants.append(variant)
                        if pathway not in results:
                            results.append(pathway)
            pathways = sorted(results, key=lambda k: k.name)
        else:
            pathways = []

        

        # Filter option for pathways for individuals_per_pathway
        #check for each pathway if there (<=,>=,==) at least n individuals per pathway
        individuals_per_pathway = request.GET.get('individuals_per_pathway')
        not_allowed = ['', None]
        if individuals_per_pathway not in not_allowed:
            new_pathways = []
            individuals_per_pathway = int(individuals_per_pathway)
            print('Individuals per pathway')
            individuals_per_pathway_option = request.GET.get('individuals_per_pathway_option', '')
            
            for pathway in pathways:
#                print pathway.name
                #count individuals
                individuals_in_pathway = []
                
#                print len(pathway.variants)
                for variant in pathway.variants:
                    if variant.individual not in individuals_in_pathway:
                        individuals_in_pathway.append(variant.individual)
                        
                #check size of individuals_in_pathway:
#                print 'individuals_in_pathway'
                if individuals_per_pathway_option == '>':
                    if len(individuals_in_pathway) >= individuals_per_pathway:
                        new_pathways.append(pathway)
            pathways = new_pathways
    else:    
        #show empty form
        form = PathwayAnalysisForm()
        variants = []
        summary = {}
        summary['has_variants'] = False
        #fake number just not to open accordion on view 
        summary['n_genes'] = 1000
        genes = []
        genes_hgmd = []
        genes_omim = []
        genes_cgd = []



    return render_to_response('pathway_analysis/analysis.html', 
        {'pathways':pathways,
        'form':form, 
        'summary':summary, 
        'query_string':query_string, 
        'filteranalysis':filteranalysis, 
        'filterconfigs':filterconfigs, 
        'genes':genes, 
        'genes_hgmd':genes_hgmd,
        'genes_omim':genes_omim,
        'genes_cgd':genes_cgd}, context_instance=RequestContext(request))

# #this method will quickly filter your data based on different criterias
# @login_required
# def get_filtered_variants(request):
#     query = {}
#     exclude = {}
#     summary = {}
#     args = []
#     query_string = request.META['QUERY_STRING']
#     new_query_string = []
#     for item in query_string.split('&'):
#         if not item.startswith('page'):
#              new_query_string.append(item)
#     query_string = "&".join(new_query_string)
    
#     print 'query string'
#     print query_string 
#     filteranalysis = FilterAnalysis.objects.all()
#     filterconfigs = FilterConfig.objects.all()
#     if query_string != [''] and query_string != '' :
#         if request.method == 'GET':
            
#             form = PathwayAnalysisForm(request.GET)
            
#             #CHR
#             chr = request.GET.get('chr', '')
#             if chr != '':
#                 query['chromossome'] = chr

#             #pos
#             pos = request.GET.get('pos', '')
#             if pos != '':
#                 pos = pos.split('-')
#                 query['pos__range'] = (pos[0], pos[1])

#             #snp_list
#             snp_list = request.GET.get('snp_list', '')
#             snp_list = snp_list.split('\r\n')
#             if snp_list[0] != u'':
#                 query['variant_id__in'] = snp_list
#             #exclude snp_list
#             exclude_snp_list = request.GET.get('exclude_snp_list', '')
#             exclude_snp_list = exclude_snp_list.split('\r\n')
#             if exclude_snp_list[0] != u'':
#                 args.append(~Q(variant_id__in=exclude_snp_list))
                
            
#             #Gene List
#             gene_list = request.GET.get('gene_list', '')
            
#             gene_list = gene_list.split('\r\n')
#             print 'gene_list'
            
#             if gene_list[0] != u'':
#                 safe_gene_list = []
#                 for row in gene_list:
#                     row = row.split(',')
#                     for item in row:
#                         safe_gene_list.append(item.strip())
#                 print safe_gene_list
#                 query['gene__in'] = safe_gene_list
            
#             #Gene group
#             genegroup_id = request.GET.get('genegroups', '')
# #            print 'GeneGroup'
# #            print genegroup_id
#             if genegroup_id != '':
#                 genegroup = GeneGroup.objects.get(id=int(genegroup_id))
#                 gene_list_group = genegroup.genes
#                 #make it possible for lines and commas #automagic
# #                print gene_list_group
#                 gene_groups = []
#                 gene_list_group = gene_list_group.split('\r\n')
#                 for row in gene_list_group:
#                     row = row.split(',')
#                     for item in row:
#                          item = item.strip()
#                          if item != "":
#                            gene_groups.append(item)
#                 query['gene__in'] = gene_groups
# #                print 'genegroup'
# #                print  gene_groups
            
#             #mutation_type
#             mutation_type = request.GET.get('mutation_type', '')
#             if mutation_type == 'homozygous':
#                 genotypes = ['0/0', './.', '0/1', '1/0', '0/2', '2/0']
#     #            exclude['genotype__in'] = genotypes 
#                 args.append(~Q(genotype__in=genotypes))
#     #            query['genotype'] = '1/1'
#             elif mutation_type == 'heterozygous':
#                 genotypes = ['0/0', './.', '1/1', '2/1', '1/2', '2/2']
#     #            ~Q(release_set__format='cd'
#                 args.append(~Q(genotype__in=genotypes))
#     #            exclude['genotype__in'] = genotypes
            
#             #exclude Gene List
#             exclude_gene_list = request.GET.get('exclude_gene_list', '')
#             exclude_gene_list = exclude_gene_list.split('\r\n')
#             if exclude_gene_list[0] != u'':
#     #            print 'exclude gene list'
#     #            print exclude_gene_list
#     #            print 'exclude gene list'
#                 args.append(~Q(gene__in=exclude_gene_list))
                
#     #            exclude['gene__in'] = exclude_gene_list
            
            
                
#             #Clinical
#             cln = request.GET.get('cln', '')
#             if cln == 'on':
#                 query['dbsnp_pm'] = 'Yes'    
                
#             #Variant type SNP EFF       
#             variant_type = request.GET.getlist('variant_type')
#             if len(variant_type) > 0:
#                 query['snp_eff__in'] = variant_type     
            
#             #DBSNP
#             dbsnp = request.GET.get('dbsnp', '')
#             if dbsnp == 'on':
#                 query['variant_id'] = "."
                
#             #1000genomes
#             genomes1000 = request.GET.get('genomes1000', '')
#             if genomes1000 != '':
#                 genomes1000_option = request.GET.get('genomes1000_option', '')
#                 if genomes1000_option == '<':
#                     #Also get null values
#                     args.append(Q(genomes1k_af__lte=float(genomes1000)) | Q(genomes1k_af__isnull=True))
#                 elif genomes1000_option == '>':
#                     args.append(Q(genomes1k_af__gte=float(genomes1000)) | Q(genomes1k_af__isnull=True))
            
#             #dbsnp Freq
#             dbsnp_frequency = request.GET.get('dbsnp_frequency', '')
#             if dbsnp_frequency != '':
#                 dbsnp_freq_option = request.GET.get('dbsnp_freq_option', '')
#                 if dbsnp_freq_option == '<':
#     #                query['dbsnp_gmaf__lte'] = float(dbsnp_frequency)
#                     args.append(Q(dbsnp_gmaf__lte=float(dbsnp_frequency)) | Q(dbsnp_gmaf__isnull=True))
#                 elif dbsnp_freq_option == '>':
#     #                query['dbsnp_gmaf__gte'] = float(dbsnp_frequency)
#                     args.append(Q(dbsnp_gmaf__gte=float(dbsnp_frequency)) | Q(dbsnp_gmaf__isnull=True))
            
#             #Exome Variation Server Freq
#             variationserver_frequency = request.GET.get('variationserver_frequency', '')
#             if variationserver_frequency != '':
#                 variationserver_option = request.GET.get('variationserver_option', '')
#                 if variationserver_option == '<':
#     #                print float(variationserver_frequency)*100.0
#     #                query['maf_total_esp5400__lte'] = float(variationserver_frequency)
#                     args.append(Q(ann_esp_maf__lte=float(variationserver_frequency)) | Q(ann_esp_maf__isnull=True))
#                 elif variationserver_option == '>':
#     #                query['maf_total_esp5400__gte'] = float(variationserver_frequency)
#                     args.append(Q(ann_esp_maf__gte=float(variationserver_frequency)) | Q(ann_esp_maf__isnull=True))
            
#             #SIFT
#             sift = request.GET.get('sift', '')
#             if sift != '':
#                 #Clinical
#                 sift_exclude = request.GET.get('sift_exclude', '')
#                 if sift_exclude == 'on':
#                     sift_flag = True
#                 else:
#                     sift_flag = False
                    
#                 sift_option = request.GET.get('sift_option', '')
#                 if sift_option == '<':
#     #                query['sift__lte'] = float(sift)
#                     if sift_flag:
#                         args.append(Q(sift__lte=float(sift)))
#                     else:
#                         args.append(Q(sift__lte=float(sift)) | Q(sift__isnull=True))
#                 elif sift_option == '>':
#                     if sift_flag:
#                         args.append(Q(sift__gte=float(sift)))
#                     else:
#                         args.append(Q(sift__gte=float(sift)) | Q(sift__isnull=True))
            
#             #POLYPHEN
#             polyphen = request.GET.get('polyphen', '')
#             if polyphen != '':
#                 polyphen_exclude = request.GET.get('polyphen_exclude', '')
#                 if polyphen_exclude == 'on':
#                     polyphen_flag = True
#                 else:
#                     polyphen_flag = False
                    
#                 polyphen_option = request.GET.get('polyphen_option', '')
#                 if polyphen_option == '<':
#                     if polyphen_flag:
#                         args.append(Q(polyphen__lte=float(polyphen)))
#                     else:
#                         args.append(Q(polyphen__lte=float(polyphen)) | Q(polyphen__isnull=True))
#                 elif polyphen_option == '>':
#                     if polyphen_flag:
#                         args.append(Q(polyphen__gte=float(polyphen)))
#                     else:
#                         args.append(Q(polyphen__gte=float(polyphen)) | Q(polyphen__isnull=True))
                    
#             #DBSNP Build
#             dbsnp_build = request.GET.get('dbsnp_build', '')
#             if dbsnp_build != '':
#                 dbsnp_option = request.GET.get('dbsnp_option', '')
#                 if dbsnp_option == '<':
#                     build_list = range(1, int(dbsnp_build))
#                     T2 = [str(x) for x in build_list]
#     #                print T2
#                     T2.append('')
#                     query['dbsnp_build__in'] = T2
#                 elif dbsnp_option == '>':
#                     build_list = range(int(dbsnp_build), 138)
#                     T2 = [str(x) for x in build_list]
#     #                print T2
#                     T2.append('')
#                     query['dbsnp_build__in'] = T2
#             #Read Depth
#             read_depth = request.GET.get('read_depth', '')
#             if read_depth != '':
#                 read_depth_option = request.GET.get('read_depth_option', '')
#                 if read_depth_option == '<':
#                     args.append(Q(read_depth__lte=int(read_depth)))
#                 elif read_depth_option == '>':
#                     args.append(Q(read_depth__gte=int(read_depth)))
            
#             #Functional class
#             func_class = request.GET.getlist('func_class')
#             if len(func_class) > 0:
#                 query['snp_eff_functional_class__in'] = func_class
#             #IMPACT           
#             impact = request.GET.getlist('impact')
#             if len(impact) > 0:
#                 query['impact__in'] = impact
            
#             print 'Exclude individuals'
#             #exclude individuals
#             exclude_individuals = request.GET.getlist('exclude_individuals')
#             print exclude_individuals
            
#             #exclude groups append to individuals
#             exclude_groups = request.GET.getlist('exclude_groups')
#             print exclude_groups
#             exclude_individuals_list = []
#             if len(exclude_groups) > 0:
#                 for group_id in exclude_groups:
#                     group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
#                     for individual in group_individuals:
#                          exclude_individuals_list.append(unicode(str(individual)))
#                     print exclude_individuals_list
                    
#             exclude_individuals_list = exclude_individuals_list + exclude_individuals
#             print exclude_individuals_list
            
#             exclude_individuals_variants = {}
            
#             #exclude variants from individuals
#             if len(exclude_individuals_list) > 0:
                
#                 #for all individuals in exclude list
#                 for individual in exclude_individuals_list:
#                     individual_variants = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values('chromossome', 'pos', 'genotype')
#                     for variant in individual_variants:
#                         id = '%s-%s' % (variant['chromossome'], variant['pos'])                        
#                         if id in exclude_individuals_variants:
#                             exclude_individuals_variants[id][variant['genotype']] = 0
#                         else:
#                             exclude_individuals_variants[id] = {}
#                             exclude_individuals_variants[id][variant['genotype']] = 0
                            
#             #INDIVIDUALS (MUST BE THE LAST ONE...) WHY ???
#             individuals = request.GET.getlist('individuals')
            
#             groups = request.GET.getlist('groups')
#             print groups
#             individuals_list = []
#             if len(groups) > 0:
#                 for group_id in groups:
#                     group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
#                     for individual in group_individuals:
#                          individuals_list.append(unicode(str(individual)))
#                     print individuals_list
                    
#             individuals_list = individuals_list + individuals
            
#             if len(individuals_list) > 0:
                 
#                 query['individual__id__in'] = individuals_list
#                 #exclude variants from individuals_list
#                 if len(exclude_individuals_list) > 0:
#     #                print 'now excluding variants from exclude_individuals'
#                     variants_ids = []
#                     #get variants from all select individuals    
#                     variants = Variant.objects.filter(*args, **query).exclude(**exclude).values('id', 'chromossome', 'pos', 'genotype')
#     #                print 'variants from selected individuals'
#     #                print variants.count() 
                    
#                     for variant in variants:
#                         id = '%s-%s' % (variant['chromossome'], variant['pos'])
#                         if id in exclude_individuals_variants:
#                             if not variant['genotype'] in exclude_individuals_variants[id]:
#                                 variants_ids.append(variant['id'])
#                         else:
#                             variants_ids.append(variant['id'])
#     #                print len(variants_ids)
#                     query['pk__in'] = variants_ids
                
                
#                 # OPTION variants per gene
#                 variants_per_gene = request.GET.get('variants_per_gene')
#                 if variants_per_gene != '':
                    
#                     variants_per_gene = int(variants_per_gene)
#     #                print 'Variants per gene'
#                     variants_per_gene_option = request.GET.get('variants_per_gene_option', '')
#                     genes_exclude_list = []
#                     for individual in individuals_list:
#     #                    print individual
#                         individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values('gene').exclude(gene="").annotate(count=Count('gene')).distinct() #.aggregate(Count('gene', distinct=True))
#     #                    print len(individual_genes)
#                         if variants_per_gene_option == '>':    
#                             for gene in individual_genes:
#                                 if gene['count'] < variants_per_gene:
#                                     genes_exclude_list.append(gene['gene'])
#                         elif variants_per_gene_option == '<':                    
#                             for gene in individual_genes:
#                                 if gene['count'] > variants_per_gene:
#                                     genes_exclude_list.append(gene['gene'])
#                         elif variants_per_gene_option == '=':
#                             for gene in individual_genes:
#                                 if gene['count'] != variants_per_gene:
#                                     genes_exclude_list.append(gene['gene'])
#                     #remove variants without gene name
#                     genes_exclude_list.append('')
                    
#                     if 'gene__in' in exclude:
#                         exclude['gene__in'] = exclude['gene__in'] + genes_exclude_list
#                     else:
#                         exclude['gene__in'] = genes_exclude_list
                    
#                 #option GENES in COMMON
#                 genes_in_common = request.GET.get('genes_in_common', '')
#                 if genes_in_common == 'on':
                    
#                     #get all genes from individual
#                     individual_gene_list = []
#                     for individual in individuals_list:
#     #                    print individual
#                         individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values_list('gene', flat=True).exclude(gene="").distinct()
#                         individual_genes = set(list(individual_genes))
#                         individual_gene_list.append(individual_genes)
#     #                print 'intersection'
#                     genes_in_common_list = set.intersection(*individual_gene_list)
#     #                print len(genes_in_common_list)
#     #                print 'genes in common'
#     #                print genes_in_common_list 
#     #                new_genes_in_common = []
#     #                if 'gene__in' in exclude:
#     #                    for item in genes_in_common_list:
#     #                        if item not in exclude['gene__in']:
#     #                            new_genes_in_common.append(item)
#     #                    genes_in_common_list = new_genes_in_common
                    
#                     query['gene__in'] = genes_in_common_list#genes_in_common_list
                    
#     #        print args
#     #        print query
#     #        print exclude
#             variants = Variant.objects.filter(*args, **query).exclude(**exclude).order_by('gene')
#             return variants

