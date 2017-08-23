from django.db.models import Q
from diseases.models import *
from diseases.models import Gene as GeneDisease
from genes.models import *
from individuals.models import *
from variants.models import *
from django.shortcuts import get_object_or_404
from django.db.models import Count

from django.http import HttpResponse
import csv
import pickle

from databases.models import VariSNP



#HERE THE FILTERS STARTS  
def filter_individuals_variants(request, query, args, exclude):
    #INDIVIDUALS
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
    print('individuals_list', individuals_list)


    #EXCLUDE individuals
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
                if str(str(individual)) not in individuals_list:
                    exclude_individuals_list.append(str(str(individual)))
    
    print('exclude_individuals_list', exclude_individuals_list)
            
    exclude_individuals_list = exclude_individuals_list + exclude_individuals
#            print exclude_individuals_list
    exclude_individuals_variants = {}
    #exclude variants from individuals
    if len(exclude_individuals_list) > 0:
        exclude_indexes = Variant.objects.filter(individual__id__in=exclude_individuals_list, *args, **query).exclude(**exclude).values_list('index', flat=True)
        exclude['index__in'] = exclude_indexes
    # print 'return individual list, exxclue', exclude['index__in']
    return individuals_list

def filter_variants_per_gene(request, query, args, exclude):
    # OPTION variants per gene
    variants_per_gene = request.GET.get('variants_per_gene', '')
    
    print('variants per gene')
    print(variants_per_gene)
    if variants_per_gene != '':
        
        variants_per_gene = int(variants_per_gene)
        variants_per_gene_option = request.GET.get('variants_per_gene_option', '')
        
        print('Debugging')
        print(variants_per_gene)
        print(variants_per_gene_option)

        genes_exclude_list = []
        genes_only_list = []
        #this works for 2 indivuduals in list and will show only genes with variants in both option on
        for individual in query['individual_id__in']:
#                        print individual
#                        print query
#                        print exclude
            print('get list of all genes for each individual')
            individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values('gene').exclude(gene="").annotate(count=Count('gene')).distinct() #.aggregate(Count('gene', distinct=True))
            print(len(individual_genes))
            if variants_per_gene_option == '>':    
                for gene in individual_genes:
                    if gene['count'] >= variants_per_gene:
                        genes_only_list.append(gene['gene'])
                    else:
                        # if genes_in_common == 'on':
                        genes_exclude_list.append(gene['gene'])
                            
            elif variants_per_gene_option == '<':                    
                for gene in individual_genes:
                    if gene['count'] <= variants_per_gene:
                        genes_only_list.append(gene['gene'])
                    else:
                        # if genes_in_common == 'on':
                        genes_exclude_list.append(gene['gene'])
            elif variants_per_gene_option == '=':
                for gene in individual_genes:
                    if gene['count'] == variants_per_gene:
                        genes_only_list.append(gene['gene'])
                    else:
                        # if genes_in_common == 'on':
                        genes_exclude_list.append(gene['gene'])
        #remove variants without gene name                    
        args.append(Q(gene__in=genes_only_list))
        args.append(~Q(gene__in=genes_exclude_list))
    
def filter_genes_in_common(request, query, args, exclude):
    #option GENES in COMMON
    print('genes in common')

    genes_in_common = request.GET.get('genes_in_common', '')
    if genes_in_common == 'on':
        #get all genes from individual
        individual_gene_list = []
        for individual in query['individual_id__in']:
            individual_genes = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values_list('gene', flat=True).exclude(gene="").distinct()
            # print 'genes finished query', len()
            individual_genes = set(list(individual_genes))
            individual_gene_list.append(individual_genes)
        genes_in_common_list = set.intersection(*individual_gene_list)                    
        query['gene__in'] = genes_in_common_list#genes_in_common_list

def filter_positions_in_common(request, query, args, exclude):
    print('positions in common')
    positions_in_common = request.GET.get('positions_in_common', '')
    if positions_in_common == 'on':
        #get all genes from individual
        individual_positions_list = []
        for individual in query['individual_id__in']:
            #should be done with an index ex. 1-2835763-C-T 'DONE :)'
            individual_positions = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values_list('pos', flat=True).distinct()
            individual_positions = set(list(individual_positions))
            individual_positions_list.append(individual_positions)
        positions_in_common_list = set.intersection(*individual_positions_list)                    
        query['pos__in'] = positions_in_common_list#genes_in_common_list

def filter_chr(request, query):
    chr = request.GET.get('chr', '')
    if chr != '':
        query['chr'] = chr

def filter_pos(request, query):
    pos = request.GET.get('pos', '')
    if pos != '':
        pos = pos.split('-')
        if len(pos) == 2:
            query['pos__range'] = (pos[0], pos[1])
        else:
            query['pos'] = pos[0]
       
def filter_snp_list(request, query, exclude):
    snp_list = request.GET.get('snp_list', '')
    snp_list = snp_list.split('\r\n')

    if snp_list[0] != '':
        safe_snp_list = []
        for row in snp_list:
            row = row.split(',')
            for item in row:
                safe_snp_list.append(item.strip())
        query['variant_id__in'] = safe_snp_list
    #exclude snp_list
    exclude_snp_list = request.GET.get('exclude_snp_list', '')
    exclude_snp_list = exclude_snp_list.split('\r\n')
    if exclude_snp_list[0] != '':
        safe_exclude_snp_list = []
        for row in exclude_snp_list:
            row = row.split(',')
            for item in row:
                safe_exclude_snp_list.append(item.strip())
        exclude['variant_id__in']=safe_exclude_snp_list#args.append(~Q(variant_id__in=safe_snp_list))

def filter_gene_list(request, query, args):
    #Gene List
    gene_list = request.GET.get('gene_list', '')
    gene_list = gene_list.split('\r\n')
#    print 'gene_list'
    if gene_list[0] != '':
        safe_gene_list = []
        for row in gene_list:
            row = row.split(',')
            for item in row:
                safe_gene_list.append(item.strip().upper())
        print(safe_gene_list)
        query['gene__in'] = safe_gene_list
    
    exclude_gene_list = request.GET.get('exclude_gene_list', '')
    exclude_gene_list = exclude_gene_list.split('\r\n')
    if exclude_gene_list[0] != '':
        safe_gene_list = []
        for row in exclude_gene_list:
            row = row.split(',')
            for item in row:
                safe_gene_list.append(item.strip().upper())
        print(safe_gene_list)
        args.append(~Q(gene__in=safe_gene_list))
    
def filter_mutation_type(request, args):

    genotype = request.GET.get('genotype', '')

    if genotype != '':
        print('genotype', genotype)
        args.append(Q(genotype=genotype))


    mutation_type = request.GET.get('mutation_type', '')
    if mutation_type == 'homozygous':
        # genotypes = ['0/0', './.', '0/1', '1/0', '0/2', '2/0']
        args.append(Q(mutation_type='HOM'))
    elif mutation_type == 'heterozygous':
        #genotypes = ['0/0', './.', '1/1', '2/1', '1/2', '2/2']
        args.append(Q(mutation_type='HET'))

def filter_effect(request, query):
    effect = request.GET.getlist('effect')
    if len(effect) > 0:
        # query['snp_eff__in'] = variant_type
        print('effect', effect)
        query['snpeff_effect__in'] = effect


def filter_dbsnp(request, query):
    dbsnp = request.GET.get('dbsnp', '')
    if dbsnp == 'on':
        query['variant_id'] = "."

def filter_varisnp(request, query, exclude):

    exclude_varisnp = request.GET.get('exclude_varisnp', '')
    if exclude_varisnp == 'on':

        snp_list = VariSNP.objects.all().values_list('dbsnp_id', flat=True)
        
        # safe_snp_list = []
        # for snp in snp_list:
        #     safe_snp_list.append(str(snp))
        # print 'snp_list', len(snp_list), snp_list[:5]
        # snp_list = list(snp_list)
        # print 'snp_list depois', len(snp_list), snp_list[:5]


        if 'variant_id__in' in exclude:
            # print 'varisnp variant_id__in ja existe!'
            # print snp_list
            exclude['variant_id__in'].extend(safe_snp_list)
        else:
            exclude['variant_id__in'] = safe_snp_list

def filter_by_1000g(request, args):
    genomes1000_exclude = request.GET.get('genomes1000_exclude', '')
    if genomes1000_exclude == 'on':
        args.append(Q(genomes1k_maf__isnull=True))
    else:
        genomes1000 = request.GET.get('genomes1000', '')
        if genomes1000 != '':
            genomes1000 = genomes1000.split(' - ')
            if len(genomes1000) == 2:
                min = float(genomes1000[0]) 
                max = float(genomes1000[1])
                args.append((Q(genomes1k_maf__lte=max) & Q(genomes1k_maf__gte=min)) | Q(genomes1k_maf__isnull=True))
            if len(genomes1000) == 1:
                max = float(genomes1000[0])
                args.append((Q(genomes1k_maf__lte=max) & Q(genomes1k_maf__gte=0)) | Q(genomes1k_maf__isnull=True))

def filter_by_dbsnp(request, args):
    dbsnp_exclude = request.GET.get('dbsnp_exclude', '')
    if dbsnp_exclude == 'on':
        args.append(Q(dbsnp_maf__isnull=True))
    else:
        dbsnp = request.GET.get('dbsnp_frequency', '')
        if dbsnp != '':
            dbsnp = dbsnp.split(' - ')
            if len(dbsnp) == 2:
                min = float(dbsnp[0]) 
                max = float(dbsnp[1])
                args.append((Q(dbsnp_maf__lte=max) & Q(dbsnp_maf__gte=min)) | Q(dbsnp_maf__isnull=True))    
            if len(dbsnp) == 1:
                max = float(dbsnp[0])
                args.append((Q(dbsnp_maf__lte=max) & Q(dbsnp_maf__gte=0)) | Q(dbsnp_maf__isnull=True))    

def filter_by_esp(request, args):
    esp_exclude = request.GET.get('esp_exclude', '')
    if esp_exclude == 'on':
        args.append(Q(esp_maf__isnull=True))
    else:
        esp = request.GET.get('esp_frequency', '')
        if esp != '':
            esp = esp.split(' - ')
            min = float(esp[0]) 
            max = float(esp[1])
            args.append((Q(esp_maf__lte=max) & Q(esp_maf__gte=min)) | Q(esp_maf__isnull=True))     
               
# def filter_genomes1000(request, args):
#     #1000genomes
#     genomes1000 = request.GET.get('genomes1000', '')
#     if genomes1000 != '':
#         genomes1000_option = request.GET.get('genomes1000_option', '')
#         if genomes1000_option == '<':
#             args.append(Q(genomes1k_maf__lte=float(genomes1000)) | Q(genomes1k_maf__isnull=True))
#         elif genomes1000_option == '>':
#             args.append(Q(genomes1k_maf__gte=float(genomes1000)) | Q(genomes1k_maf__isnull=True))
#         elif genomes1000_option == '=':
#             args.append(Q(genomes1k_maf=float(genomes1000)))

# def filter_dbsnp_frequency(request, args):
#     #dbsnp Freq
#     dbsnp_frequency = request.GET.get('dbsnp_frequency', '')
#     if dbsnp_frequency != '':
#         dbsnp_freq_option = request.GET.get('dbsnp_freq_option', '')
#         if dbsnp_freq_option == '<':
#             args.append(Q(dbsnp_maf__lte=float(dbsnp_frequency)) | Q(dbsnp_maf__isnull=True))
#         elif dbsnp_freq_option == '>':
#             args.append(Q(dbsnp_maf__gte=float(dbsnp_frequency)) | Q(dbsnp_maf__isnull=True))
#         elif dbsnp_freq_option == '=':    
#             args.append(Q(dbsnp_maf=float(dbsnp_frequency)))
# def filter_variationserver_frequency(request, args):
#     #Exome Variation Server Freq
#     variationserver_frequency = request.GET.get('variationserver_frequency', '')
#     if variationserver_frequency != '':
#         variationserver_option = request.GET.get('variationserver_option', '')
#         if variationserver_option == '<':
#             args.append(Q(esp_maf__lte=float(variationserver_frequency)) | Q(esp_maf__isnull=True))
#         elif variationserver_option == '>':
#             args.append(Q(esp_maf__gte=float(variationserver_frequency)) | Q(esp_maf__isnull=True))
#         elif variationserver_option == '=':
#             args.append(Q(esp_maf=float(variationserver_frequency)))


def filter_by_individuals(request, args, query, exclude):
    #INDIVIDUALS
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
    print('individuals_list', individuals_list)


    #EXCLUDE individuals
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
                if str(str(individual)) not in individuals_list:
                    exclude_individuals_list.append(str(str(individual)))
    
    print('exclude_individuals_list', exclude_individuals_list)
            
    exclude_individuals_list = exclude_individuals_list + exclude_individuals
#            print exclude_individuals_list
    exclude_individuals_variants = {}
    #exclude variants from individuals
    if len(exclude_individuals_list) > 0:
        exclude_indexes = Variant.objects.filter(individual__id__in=exclude_individuals_list, *args, **query).exclude(**exclude).values_list('index', flat=True)
        exclude['index__in'] = exclude_indexes


    if len(individuals_list) > 0:
        #only add to query after filtering the indexes 
        query['individual_id__in'] = individuals_list
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
                if variants_per_gene_option == '>':    
                    for gene in individual_genes:
                        if gene['count'] >= variants_per_gene:
                            genes_only_list.append(gene['gene'])
                        else:
                            # if genes_in_common == 'on':
                            genes_exclude_list.append(gene['gene'])
                                
                elif variants_per_gene_option == '<':                    
                    for gene in individual_genes:
                        if gene['count'] <= variants_per_gene:
                            genes_only_list.append(gene['gene'])
                        else:
                            # if genes_in_common == 'on':
                            genes_exclude_list.append(gene['gene'])
                elif variants_per_gene_option == '=':
                    for gene in individual_genes:
                        if gene['count'] == variants_per_gene:
                            genes_only_list.append(gene['gene'])
                        else:
                            # if genes_in_common == 'on':
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
                #should be done with an index ex. 1-2835763-C-T 'DONE :)'
                individual_positions = Variant.objects.filter(individual__id=individual, *args, **query).exclude(**exclude).values_list('pos', flat=True).distinct()
                individual_positions = set(list(individual_positions))
                individual_positions_list.append(individual_positions)
            positions_in_common_list = set.intersection(*individual_positions_list)                    
            query['pos__in'] = positions_in_common_list#genes_in_common_list

    


    
    


def filter_qual(request, args):
    qual = request.GET.get('qual', '')
    if qual != '':
        qual_option = request.GET.get('qual_option', '')
        if qual_option == '<':
            args.append(Q(qual__lte=float(qual)))
        elif qual_option == '>':
            args.append(Q(qual__gte=float(qual)))
        elif qual_option == '=':
            args.append(Q(qual=float(qual)))


def filter_filter(request, query):     
    filter = request.GET.getlist('filter')
    if len(filter) > 0:
        query['filter__in'] = filter

def filter_by_sift(request, args):
    sift = request.GET.get('sift', '')
    if sift != '':
        sift_exclude = request.GET.get('sift_exclude', '')
        if sift_exclude == 'on':
            sift_flag = True
        else:
            sift_flag = False
        sift = sift.split(' - ')
        sift_min = float(sift[0]) 
        sift_max = float(sift[1])
        if sift_flag:
            args.append(Q(sift__lte=sift_max) & Q(sift__gte=sift_min))
        else:
            args.append((Q(sift__lte=sift_max) & Q(sift__gte=sift_min)) | Q(sift__isnull=True))
def filter_by_cadd(request, args):
    cadd = request.GET.get('cadd', '')
    if cadd != '':
        cadd_exclude = request.GET.get('cadd_exclude', '')
        if cadd_exclude == 'on':
            cadd_flag = True
            # print('CADD Flag on')
        else:
            cadd_flag = False
        cadd = cadd.split(' - ')
        cadd_min = float(cadd[0]) 
        cadd_max = float(cadd[1])
        # print('CADD', cadd_min, cadd_max)
        if cadd_flag:
            args.append(Q(cadd__lte=cadd_max) & Q(cadd__gte=cadd_min))
        else:
            args.append((Q(cadd__lte=cadd_max) & Q(cadd__gte=cadd_min)) | Q(cadd__isnull=True))

def filter_by_mcap(request, args):
    mcap = request.GET.get('mcap', '')
    if mcap != '':
        mcap_exclude = request.GET.get('mcap_exclude', '')
        if mcap_exclude == 'on':
            mcap_flag = True
            # print('CADD Flag on')
        else:
            mcap_flag = False
        mcap = mcap.split(' - ')
        mcap_min = float(mcap[0]) 
        mcap_max = float(mcap[1])
        # print('CADD', cadd_min, cadd_max)
        if mcap_flag:
            args.append(Q(mcap_score__lte=mcap_max) & Q(mcap_score__gte=mcap_min))
        else:
            args.append((Q(mcap_score__lte=mcap_max) & Q(mcap_score__gte=mcap_min)) | Q(mcap_score__isnull=True))
                   
def filter_by_rf_score(request, args):
    rf_score = request.GET.get('rf_score', '')
    if rf_score != '':
        rf_exclude = request.GET.get('rf_exclude', '')
        if rf_exclude == 'on':
            rf_flag = True
        else:
            rf_flag = False
        rf = rf_score.split(' - ')
        rf_min = float(rf[0]) 
        rf_max = float(rf[1])
        if rf_flag:
            args.append(Q(rf_score__lte=rf_max) & Q(rf_score__gte=rf_min))
        else:
            args.append((Q(rf_score__lte=rf_max) & Q(rf_score__gte=rf_min)) | Q(rf_score__isnull=True))            
def filter_by_ada_score(request, args):
    ada_score = request.GET.get('ada_score', '')
    if ada_score != '':
        ada_exclude = request.GET.get('ada_exclude', '')
        if ada_exclude == 'on':
            ada_flag = True
        else:
            ada_flag = False
        ada = ada_score.split(' - ')
        ada_min = float(ada[0]) 
        ada_max = float(ada[1])
        if ada_flag:
            args.append(Q(ada_score__lte=ada_max) & Q(ada_score__gte=ada_min))
        else:
            args.append((Q(ada_score__lte=ada_max) & Q(ada_score__gte=ada_min)) | Q(ada_score__isnull=True))            
            
def filter_by_pp2(request, args):
    polyphen = request.GET.get('polyphen', '')
    if polyphen != '':
        polyphen_exclude = request.GET.get('polyphen_exclude', '')
        if polyphen_exclude == 'on':
            polyphen_flag = True
        else:
            polyphen_flag = False
        polyphen = polyphen.split(' - ')
        polyphen_min = float(polyphen[0]) 
        polyphen_max = float(polyphen[1])
        if polyphen_flag:
            args.append(Q(polyphen2__lte=polyphen_max) & Q(polyphen2__gte=polyphen_min))
        else:
            args.append((Q(polyphen2__lte=polyphen_max) & Q(polyphen2__gte=polyphen_min)) | Q(polyphen2__isnull=True))


# def filter_by_hi_score(request, args):
#     hi_exclude = request.GET.get('hi_exclude', '')
#     if hi_exclude == 'on':
#         args.append(Q(hi_score_perc__isnull=False))
    
#     hi = request.GET.get('hi_frequency', '')
#     if hi != '':
#         hi = hi.split(' - ')
#         min = float(hi[0]) 
#         max = float(hi[1])
#         args.append((Q(hi_score_perc__lte=max) & Q(hi_score_perc__gte=min)))
#         #| Q(hi_score_perc__isnull=True)




def filter_by_segdup(request, args):
    exclude_segdup = request.GET.get('exclude_segdup', '')
    if exclude_segdup == 'on':
        args.append(Q(segdup=''))


def filter_cgd(request, args):
    cgdmanifestation = request.GET.getlist('cgdmanifestation')
    # interventions = request.GET.getlist('interventions')
    conditions = request.GET.getlist('cgd')
    # print 'FILTER BY CGD'
    # print manifestations, interventions
    if len(cgdmanifestation) > 0:
        if cgdmanifestation[0] != '':
            #get a list of CGDENTRY
            cgdentries = CGDEntry.objects.filter(MANIFESTATION_CATEGORIES__in=cgdmanifestation)
            gene_list = []
            for gene in cgdentries:
                gene_list.append(gene.GENE)
            args.append(Q(gene__in=gene_list))
    if len(conditions) > 0:
        if conditions[0] != '':
            cgdentries = CGDEntry.objects.filter(CONDITIONS__in=conditions)
            gene_list = []
            for gene in cgdentries:
                gene_list.append(gene.GENE)
            args.append(Q(gene__in=gene_list))



def filter_omim(request, args):
    omim = request.GET.getlist('omim')
    print('omim', omim)
    # print 'FILTER BY CGD'
    # print manifestations, interventions
    print('FILTER OMIM')
    if len(omim) > 0:
        if omim[0] != '':
            omimentries = Disease.objects.filter(id__in=omim)
            gene_list = []
            print('omimentries', omimentries)

            genes = GeneDisease.objects.filter(diseases__in=omimentries)
            print('omimgenes', genes)
            for gene in genes:
                gene_list.append(gene.official_name)
            args.append(Q(gene__in=gene_list))

def filter_hgmd(request, args):
    hgmd = request.GET.getlist('hgmd')
    # print 'omim', omim
    # print 'FILTER BY CGD'
    # print manifestations, interventions
    # print 'FILTER OMIM'
    if len(hgmd) > 0:
        if hgmd[0] != '':
            hgmdentries = HGMDPhenotype.objects.filter(id__in=hgmd)
            gene_list = []
            # print 'hgmdentries', hgmdentries
            genes = HGMDGene.objects.filter(diseases__in=hgmdentries)
            # print 'hgmdgenes', genes
            for gene in genes:
                gene_list.append(gene.symbol)
            args.append(Q(gene__in=gene_list))

def filter_genelists(request, query, args, exclude):
    genelists = request.GET.getlist('genelists')

    safe_gene_list = []
    if len(genelists) > 0:
        
        for genelist_id in genelists:
            genelist_obj = GeneList.objects.get(pk=genelist_id)
            # print 'genelist'
            # print genelist_obj.genes
            gene_list = genelist_obj.genes.split(',')
            for gene in gene_list:
                if gene not in safe_gene_list:
                    safe_gene_list.append(gene.upper())
        query['gene__in'] = safe_gene_list


        # gene_list = gene_list.split('\r\n')
        # # print 'gene_list'
        # if gene_list[0] != u'':
            
        #     for row in gene_list:
        #         row = row.split(',')
        #         for item in row:
        #             gene = item.strip()
        #             if (gene != ' ' and gene != ''):
        #                 if gene not in safe_gene_list:
        #                     safe_gene_list.append(item.strip())
    

    exclude_genelists = request.GET.getlist('exclude_genelists')
    if len(exclude_genelists) > 0:
        exclude_safe_gene_list = []
        for genelist_id in exclude_genelists:
            genelist_obj = GeneList.objects.get(pk=genelist_id)
            gene_list = genelist_obj.genes.split(',')
            for gene in gene_list:
                if gene not in safe_gene_list:
                    if gene not in exclude_safe_gene_list:
                        exclude_safe_gene_list.append(gene)
        if len(exclude_safe_gene_list) > 0:
            exclude['gene__in'] = exclude_safe_gene_list

        # # print 'genelist'
        # # print genelist_obj.genes
        # gene_list = genelist_obj.genes

        # gene_list = gene_list.split('\r\n')
        # # print 'gene_list'
        # if gene_list[0] != u'':
            
        #     for row in gene_list:
        #         row = row.split(',')
        #         for item in row:
        #             gene = item.strip()
        #             if (gene != ' ' and gene != ''):
        #                 if gene not in exclude_safe_gene_list:
        #                     exclude_safe_gene_list.append(item.strip())
    # query['gene__nin'] = safe_gene_list


    # print 'safe_gene_list'
    # print len(safe_gene_list)
    # print safe_gene_list
    # query['gene__in'] = safe_gene_list

    # args.append(Q(gene__in=safe_gene_list))



#HERE STARTS FILTER FOR FAMILY ANALYSIS
def filter_inheritance_option(request):
    inheritance_option = request.GET.get('inheritance_option', '')

    if inheritance_option == '3':
        request.GET.__setitem__('variants_per_gene','2')
        request.GET.__setitem__('variants_per_gene_option','>')
        print(request.GET)
        

def filter_inheritance_option_exclude_individuals(request):
    inheritance_option = request.GET.get('inheritance_option', '')
    exclude_individuals = request.GET.getlist('exclude_individuals')
    father = request.GET.get('father', '')
    mother = request.GET.get('mother', '')
    parents = [father, mother]
    if inheritance_option == '1' or inheritance_option == '2':
        if father not in exclude_individuals:
            request.GET.appendlist('exclude_individuals', father)
        if mother not in exclude_individuals:
            request.GET.appendlist('exclude_individuals', mother)
            
def filter_inheritance_option_mutation_type(request, args):
    inheritance_option = request.GET.get('inheritance_option', '')
    #by exclusion of genotypes
    if inheritance_option == '1':
        genotypes = ['0/0', './.', '0/1', '1/0', '0/2', '2/0']
        args.append(~Q(genotype__in=genotypes))

def filter_sift(request, args):
    sift = request.GET.get('sift', '')
    if sift != '':
        sift_exclude = request.GET.get('sift_exclude', '')
        if sift_exclude == 'on':
            sift_flag = True
        else:
            sift_flag = False
        sift_option = request.GET.get('sift_option', '')
        if sift_option == '<':
            if sift_flag:
                args.append(Q(sift__lte=float(sift)))
            else:
                args.append(Q(sift__lte=float(sift)) | Q(sift__isnull=True))
        elif sift_option == '>':
            if sift_flag:
                args.append(Q(sift__gte=float(sift)))
            else:
                args.append(Q(sift__gte=float(sift)) | Q(sift__isnull=True))
        elif sift_option == '=':
            if sift_flag:
                args.append(Q(sift=float(sift)))
            else:
                args.append(Q(sift=float(sift)) | Q(sift__isnull=True))

def filter_polyphen2(request, args):
    polyphen = request.GET.get('polyphen', '')
    if polyphen != '':
        polyphen_exclude = request.GET.get('polyphen_exclude', '')
        if polyphen_exclude == 'on':
            polyphen_flag = True
        else:
            polyphen_flag = False
            
        polyphen_option = request.GET.get('polyphen_option', '')
        if polyphen_option == '<':
            if polyphen_flag:
                args.append(Q(polyphen2__lte=float(polyphen)))
            else:
                args.append(Q(polyphen2__lte=float(polyphen)) | Q(polyphen2__isnull=True))
        elif polyphen_option == '>':
            if polyphen_flag:
                args.append(Q(polyphen2__gte=float(polyphen)))
            else:
                args.append(Q(polyphen2__gte=float(polyphen)) | Q(polyphen2__isnull=True))
        elif polyphen_option == '=':
            if polyphen_flag:
                args.append(Q(polyphen2=float(polyphen)))
            else:
                args.append(Q(polyphen2=float(polyphen)) | Q(polyphen2__isnull=True))
def filter_dbsnp_build(request, args):
    dbsnp_build = request.GET.get('dbsnp_build', '')
    if dbsnp_build != '':
        dbsnp_option = request.GET.get('dbsnp_option', '')
        if dbsnp_option == '<':
            # build_list = range(1, int(dbsnp_build))
            # T2 = [str(x) for x in build_list]
            # T2.append('')
            # query['dbsnp_build__in'] = #T2
            args.append(Q(dbsnp_build__lte=int(dbsnp_build)) | Q(dbsnp_build__isnull=True))
        elif dbsnp_option == '>':
            # build_list = range(int(dbsnp_build), 138)
            # T2 = [str(x) for x in build_list]
            # T2.append('')
            # query['dbsnp_build__in'] = T2
            args.append(Q(dbsnp_build__gte=int(dbsnp_build)) | Q(dbsnp_build__isnull=True))

def filter_read_depth(request, args):
    read_depth = request.GET.get('read_depth', '')
    if read_depth != '':
        read_depth_option = request.GET.get('read_depth_option', '')
        if read_depth_option == '<':
            args.append(Q(read_depth__lte=int(read_depth)))
        elif read_depth_option == '>':
            args.append(Q(read_depth__gte=int(read_depth)))
        elif read_depth_option == '=':
            args.append(Q(read_depth=int(read_depth)))

                        
def filter_func_class(request, query):
    func_class = request.GET.getlist('func_class')
    if len(func_class) > 0:
        query['snpeff_func_class__in'] = func_class
        # query['effect__in'] = variant_type

def filter_impact(request, query):     
    impact = request.GET.getlist('impact')
    if len(impact) > 0:
        # query['snpeff__impact__in'] = impact
        query['snpeff_impact__in'] = impact
def filter_is_at_hgmd(request, query):     
    # hgmd = request.GET.getlist('is_at_hgmd')
    hgmd = request.GET.get('is_at_hgmd', '')
    if hgmd == 'on':
        query['is_at_hgmd'] = True

def filter_clnsig(request, query):     
    # hgmd = request.GET.getlist('is_at_hgmd')
    clnsig = request.GET.get('clnsig', '')
    if clnsig != '':
        query['clinvar_clnsig'] = clnsig



def export_to_csv(request, variants):
    #export to csv
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
        writer.writerow(['Individual', 'Index', 'Pos_index', 'Chr', 'Pos', 'Variant_id', 'Ref', 'Alt', 'Qual', 'Filter', 'Info', 'Format', 'Genotype_col', 'Genotype', 'Read_depth', 'Gene', 'Mutation_type', 'Vartype', 'Genomes1k_maf', 'Dbsnp_maf', 'Esp_maf', 'Dbsnp_build', 'Sift', 'Sift_pred', 'Polyphen2', 'Polyphen2_pred', 'Condel', 'Condel_pred', 'DANN', 'CADD', 'Is_at_omim', 'Is_at_hgmd', 'Hgmd_entries', 'Effect', 'Impact', 'Func_class', 'Codon_change', 'Aa_change', 'Aa_len', 'Gene_name', 'Biotype', 'Gene_coding', 'Transcript_id', 'Exon_rank', 'Genotype_number', 'Allele', 'Gene', 'Feature', 'Feature_type', 'Consequence', 'Cdna_position', 'Cds_position', 'Protein_position', 'Amino_acids', 'Codons', 'Existing_variation', 'Distance', 'Strand', 'Symbol', 'Symbol_source', 'Sift', 'Polyphen', 'Condel']) 
        for variant in variants:
            # print 'variant', variant.index
            writer.writerow([variant.individual, variant.index, variant.pos_index, variant.chr, variant.pos, variant.variant_id, variant.ref, variant.alt, variant.qual, variant.filter, pickle.loads(variant.info), variant.format, variant.genotype_col, variant.genotype, variant.read_depth, variant.gene, variant.mutation_type, variant.vartype, variant.genomes1k_maf, variant.dbsnp_maf, variant.esp_maf, variant.dbsnp_build, variant.sift, variant.sift_pred, variant.polyphen2, variant.polyphen2_pred, variant.condel, variant.condel_pred, variant.dann, variant.cadd, variant.is_at_omim, variant.is_at_hgmd, variant.hgmd_entries])
        return response
