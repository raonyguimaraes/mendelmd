import csv
import pickle
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from diseases.models import Disease, HGMDPhenotype, HGMDGene
from diseases.models import Gene as GeneDisease

from genes.models import CGDEntry, GeneList

from individuals.models import Group

from variants.models import Variant

from databases.models import VariSNP

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q as EQ
from elasticsearch_dsl import Search

ES = Elasticsearch(hosts=[{'host': 'es01', 'port': 9200}])


# HERE THE FILTERS STARTS
def filter_individuals_variants(request, query, args, exclude, args_es):
    # INDIVIDUALS
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

    # EXCLUDE individuals
    exclude_individuals = request.GET.getlist('exclude_individuals')

    # exclude groups append to individuals
    exclude_groups = request.GET.getlist('exclude_groups')

    exclude_individuals_list = []
    if len(exclude_groups) > 0:
        for group_id in exclude_groups:
            group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
            for individual in group_individuals:
                if str(str(individual)) not in individuals_list:
                    exclude_individuals_list.append(str(str(individual)))

    print('exclude_individuals_list', exclude_individuals_list)

    exclude_individuals_list = exclude_individuals_list + exclude_individuals
    exclude_individuals_variants = {}
    # exclude variants from individuals
    if len(exclude_individuals_list) > 0:
        exclude_indexes = Variant.objects.filter(
            individual__id__in=exclude_individuals_list, *args, **query
        ).exclude(**exclude).values_list('index', flat=True)
        exclude['index__in'] = exclude_indexes
    # print 'return individual list, exxclue', exclude['index__in']
    return individuals_list


def filter_variants_per_gene(request, query: dict, args: list, exclude: dict, args_es: list) -> None:
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
        # this works for 2 indivuduals in list and will show only genes with variants in both option on
        for individual in query['individual_id__in']:
            print('get list of all genes for each individual')
            individual_genes = Variant.objects.filter(
                individual__id=individual, *args, **query
            ).exclude(
                **exclude
            ).values('gene').exclude(gene="").annotate(count=Count('gene')).distinct()
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
        # remove variants without gene name
        args.append(Q(gene__in=genes_only_list))
        args.append(~Q(gene__in=genes_exclude_list))


def filter_genes_in_common(request, query: dict, args: list, exclude: dict, args_es: list) -> None:
    # option GENES in COMMON
    print('genes in common')

    genes_in_common = request.GET.get('genes_in_common', '')
    if genes_in_common == 'on':
        # get all genes from individual
        individual_gene_list = []
        individual_gene_list_es = []
        for individual in query['individual_id__in']:
            print(f"ARGS_ES: {args_es}")
            individual_genes = Variant.objects.filter(
                individual__id=individual, *args, **query
            ).exclude(**exclude).values_list('gene', flat=True).exclude(gene="").distinct()
            individual_genes_es = Search(
                using=ES, index="variant-index"
            ).filter(
                EQ('match', individual=individual)
            ).query(EQ('bool', must=args_es)).execute()
            list_genes_es = [indi_genes.gene for indi_genes in individual_genes_es]
            # print 'genes finished query', len()
            individual_genes = set(list(individual_genes))
            individual_gene_list.append(individual_genes)
            individual_gene_list_es.extend(list_genes_es)
        genes_in_common_list = set.intersection(*individual_gene_list)
        query['gene__in'] = genes_in_common_list  # genes_in_common_list
        should_list = [EQ("match_phrase", gene=gene_) for gene_ in individual_gene_list_es]
        args_es.append(EQ('bool', should=should_list, minimum_should_match=1))


def filter_positions_in_common(request, query: dict, args: list, exclude: dict, args_es: list) -> None:
    print('positions in common')
    positions_in_common = request.GET.get('positions_in_common', '')
    if positions_in_common == 'on':
        # get all genes from individual
        individual_positions_list = []
        for individual in query['individual_id__in']:
            # should be done with an index ex. 1-2835763-C-T 'DONE :)'
            individual_positions = Variant.objects.filter(
                individual__id=individual, *args, **query
            ).exclude(**exclude).values_list('pos', flat=True).distinct()

            individual_positions = set(list(individual_positions))
            individual_positions_list.append(individual_positions)
        positions_in_common_list = set.intersection(*individual_positions_list)
        query['pos__in'] = positions_in_common_list  # genes_in_common_list


def filter_chr(request, query, args_es):
    chr = request.GET.get('chr', '')
    if chr != '':
        query['chr'] = chr
        args_es.append(EQ('match', chr=chr))


def filter_pos(request, query, args_es):
    pos = request.GET.get('pos', '')
    if pos != '':
        pos = pos.split('-')
        if len(pos) == 2:
            query['pos__range'] = (pos[0], pos[1])
            args_es.append(EQ("range", pos={"lte": pos[1], "gte": pos[0]}))
        else:
            query['pos'] = pos[0]
            args_es.append(EQ('match', pos=pos[0]))


def filter_snp_list(request, query, exclude, args_es):
    snp_list = request.GET.get('snp_list', '')
    snp_list = snp_list.split('\r\n')

    if snp_list[0] != '':
        safe_snp_list = []
        for row in snp_list:
            row = row.split(',')
            for item in row:
                safe_snp_list.append(item.strip())
        query['variant_id__in'] = safe_snp_list
        args_es.append(EQ("match", variant_id=str(safe_snp_list)))

    # exclude snp_list
    exclude_snp_list = request.GET.get('exclude_snp_list', '')
    exclude_snp_list = exclude_snp_list.split('\r\n')
    if exclude_snp_list[0] != '':
        safe_exclude_snp_list = []
        for row in exclude_snp_list:
            row = row.split(',')
            for item in row:
                safe_exclude_snp_list.append(item.strip())
        exclude['variant_id__in'] = safe_exclude_snp_list  # args.append(~Q(variant_id__in=safe_snp_list))
        args_es.append(~EQ("match", variant_id=str(safe_exclude_snp_list)))


def filter_gene_list(request, query, args, args_es):
    # Gene List
    gene_list = request.GET.get('gene_list', '')
    gene_list = gene_list.split('\r\n')

    if gene_list[0] != '':
        safe_gene_list = []
        for row in gene_list:
            row = row.split(',')
            for item in row:
                safe_gene_list.append(item.strip().upper())
        print(safe_gene_list)
        query['gene__in'] = safe_gene_list
        args_es.append(EQ("match", gene=str(safe_gene_list)))

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
        args_es.append(~EQ("match", gene=str(safe_gene_list)))


def filter_mutation_type(request, args, args_es):
    genotype = request.GET.get('genotype', '')

    if genotype != '':
        print('genotype', genotype)
        args.append(Q(genotype=genotype))
        args_es.append(EQ("match_phrase", genotype=genotype))

    mutation_type = request.GET.get('mutation_type', '')
    if mutation_type == 'homozygous':
        # genotypes = ['0/0', './.', '0/1', '1/0', '0/2', '2/0']
        args.append(Q(mutation_type='HOM'))
        args_es.append(EQ("match_phrase", mutation_type='HOM'))
    elif mutation_type == 'heterozygous':
        # genotypes = ['0/0', './.', '1/1', '2/1', '1/2', '2/2']
        args.append(Q(mutation_type='HET'))
        args_es.append(EQ("match_phrase", mutation_type='HET'))


def filter_effect(request, query, args_es):
    effect = request.GET.getlist('effect')
    if len(effect) > 0:
        print('effect', effect)
        query['snpeff_effect__in'] = effect
        should_list = [EQ("match_phrase", snpeff_effect=item_) for item_ in effect]
        args_es.append(EQ('bool', should=should_list, minimum_should_match=1))


def filter_dbsnp(request, query, args_es):
    # ToDo: Can't findo '.' character have to analyse the index steps
    dbsnp = request.GET.get('dbsnp', '')
    if dbsnp == 'on':
        query['variant_id'] = "."
        args_es.append(EQ("match_phrase", variant_id='.'))


def filter_varisnp(request, query, exclude, args_es):
    exclude_varisnp = request.GET.get('exclude_varisnp', '')
    if exclude_varisnp == 'on':
        snp_list = VariSNP.objects.all().values_list('dbsnp_id', flat=True)

        safe_snp_list = [str(snp) for snp in snp_list]

        if 'variant_id__in' in exclude:
            exclude['variant_id__in'].extend(safe_snp_list)
        else:
            exclude['variant_id__in'] = safe_snp_list
        args_es.append(~EQ("match", variant_id=str(safe_snp_list)))


def filter_by_1000g(request, args, args_es):
    genomes1000_exclude = request.GET.get('genomes1000_exclude', '')
    if genomes1000_exclude == 'on':
        args.append(Q(genomes1k_maf__isnull=True))
        args_es.append(~EQ("exists", field='genomes1k_maf'))
    else:
        genomes1000 = request.GET.get('genomes1000', '')
        if genomes1000 != '':
            genomes1000 = genomes1000.split(' - ')
            min = max = 0
            if len(genomes1000) == 2:
                min = float(genomes1000[0])
                max = float(genomes1000[1])
            if len(genomes1000) == 1:
                max = float(genomes1000[0])
            args.append((Q(genomes1k_maf__lte=max) & Q(genomes1k_maf__gte=min)) | Q(genomes1k_maf__isnull=True))
            args_es.append(EQ("range", genomes1k_maf={"lte": max, "gte": min}) | ~EQ("exists", field='genomes1k_maf'))


def filter_by_dbsnp(request, args, args_es):
    dbsnp_exclude = request.GET.get('dbsnp_exclude', '')
    if dbsnp_exclude == 'on':
        args.append(Q(dbsnp_maf__isnull=True))
        args_es.append(~EQ("exists", field='dbsnp_maf'))
    else:
        dbsnp = request.GET.get('dbsnp_frequency', '')
        if dbsnp != '':
            dbsnp = dbsnp.split(' - ')
            min = max = 0
            if len(dbsnp) == 2:
                min = float(dbsnp[0])
                max = float(dbsnp[1])
            if len(dbsnp) == 1:
                max = float(dbsnp[0])
            args.append((Q(dbsnp_maf__lte=max) & Q(dbsnp_maf__gte=min)) | Q(dbsnp_maf__isnull=True))
            args_es.append(EQ("range", dbsnp_maf={"lte": max, "gte": min}) | ~EQ("exists", field='dbsnp_maf'))


def filter_by_esp(request, args, args_es):
    esp_exclude = request.GET.get('esp_exclude', '')
    if esp_exclude == 'on':
        args.append(Q(esp_maf__isnull=True))
        args_es.append(~EQ("exists", field='esp_maf'))
    else:
        esp = request.GET.get('esp_frequency', '')
        if esp != '':
            esp = esp.split(' - ')
            min = float(esp[0])
            max = float(esp[1])
            args.append((Q(esp_maf__lte=max) & Q(esp_maf__gte=min)) | Q(esp_maf__isnull=True))
            args_es.append(EQ("range", esp_maf={"lte": max, "gte": min}) | ~EQ("exists", field='esp_maf'))


def filter_by_individuals(request, args, query, exclude):
    # ToDo: Refactor this method before change it to ElasticSearch
    # INDIVIDUALS
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

    # EXCLUDE individuals
    exclude_individuals = request.GET.getlist('exclude_individuals')

    # exclude groups append to individuals
    exclude_groups = request.GET.getlist('exclude_groups')

    exclude_individuals_list = []
    if len(exclude_groups) > 0:
        for group_id in exclude_groups:
            group_individuals = get_object_or_404(Group, pk=group_id).members.values_list('id', flat=True)
            for individual in group_individuals:
                if str(str(individual)) not in individuals_list:
                    exclude_individuals_list.append(str(str(individual)))

    print('exclude_individuals_list', exclude_individuals_list)

    exclude_individuals_list = exclude_individuals_list + exclude_individuals
    exclude_individuals_variants = {}
    # exclude variants from individuals
    if len(exclude_individuals_list) > 0:
        exclude_indexes = Variant.objects.filter(
            individual__id__in=exclude_individuals_list, *args, **query
        ).exclude(**exclude).values_list('index', flat=True)
        exclude['index__in'] = exclude_indexes

    if len(individuals_list) > 0:
        # only add to query after filtering the indexes
        query['individual_id__in'] = individuals_list
        # OPTION variants per gene
        variants_per_gene = request.GET.get('variants_per_gene')
        # option GENES in COMMON
        genes_in_common = request.GET.get('genes_in_common', '')

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
            # this works for 2 indivuduals in list and with show only genes with variants in both option on
            for individual in individuals_list:
                print('get list of all genes for each individual')
                individual_genes = Variant.objects.filter(
                    individual__id=individual, *args, **query
                ).exclude(**exclude).values(
                    'gene'
                ).exclude(gene="").annotate(count=Count('gene')).distinct()
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
            # remove variants without gene name
            args.append(Q(gene__in=genes_only_list))
            args.append(~Q(gene__in=genes_exclude_list))

        if genes_in_common == 'on':
            # get all genes from individual
            individual_gene_list = []
            for individual in individuals_list:
                individual_genes = Variant.objects.filter(
                    individual__id=individual, *args, **query
                ).exclude(**exclude).values_list('gene', flat=True).exclude(gene="").distinct()
                individual_genes = set(list(individual_genes))
                individual_gene_list.append(individual_genes)
            genes_in_common_list = set.intersection(*individual_gene_list)
            query['gene__in'] = genes_in_common_list  # genes_in_common_list

        positions_in_common = request.GET.get('positions_in_common', '')
        if positions_in_common == 'on':
            # get all genes from individual
            individual_positions_list = []
            for individual in individuals_list:
                # should be done with an index ex. 1-2835763-C-T 'DONE :)'
                individual_positions = Variant.objects.filter(
                    individual__id=individual, *args, **query
                ).exclude(**exclude).values_list('pos', flat=True).distinct()
                individual_positions = set(list(individual_positions))
                individual_positions_list.append(individual_positions)
            positions_in_common_list = set.intersection(*individual_positions_list)
            query['pos__in'] = positions_in_common_list  # genes_in_common_list


def filter_qual(request, args, args_es):
    qual = request.GET.get('qual', '')
    if qual != '':
        qual_option = request.GET.get('qual_option', '')
        if qual_option == '<':
            args.append(Q(qual__lte=float(qual)))
            args_es.append(EQ("range", qual={"lte": float(qual)}))
        elif qual_option == '>':
            args.append(Q(qual__gte=float(qual)))
            args_es.append(EQ("range", qual={"gte": float(qual)}))
        elif qual_option == '=':
            args.append(Q(qual=float(qual)))
            args_es.append(EQ("match", qual=float(qual)))


def filter_filter(request, query, args_es):
    filter = request.GET.getlist('filter')
    if len(filter) > 0:
        query['filter__in'] = filter
        should_list = [EQ("match_phrase", filter=filter_) for filter_ in filter]
        args_es.append(EQ('bool', should=should_list, minimum_should_match=1))


def filter_by_sift(request, args, args_es):
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
            args_es.append(EQ("range", shift={"lte": sift_max, "gte": sift_min}))
        else:
            args.append((Q(sift__lte=sift_max) & Q(sift__gte=sift_min)) | Q(sift__isnull=True))
            args_es.append(EQ("range", shift={"lte": sift_max, "gte": sift_min}) | ~EQ("exists", field='shift'))


def filter_by_cadd(request, args, args_es):
    cadd = request.GET.get('cadd', '')
    if cadd != '':
        cadd_exclude = request.GET.get('cadd_exclude', '')
        if cadd_exclude == 'on':
            cadd_flag = True
        else:
            cadd_flag = False
        cadd = cadd.split(' - ')
        cadd_min = float(cadd[0])
        cadd_max = float(cadd[1])
        if cadd_flag:
            args.append(Q(cadd__lte=cadd_max) & Q(cadd__gte=cadd_min))
            args_es.append(EQ("range", cadd={"lte": cadd_max, "gte": cadd_min}))
        else:
            args.append((Q(cadd__lte=cadd_max) & Q(cadd__gte=cadd_min)) | Q(cadd__isnull=True))
            args_es.append(EQ("range", cadd={"lte": cadd_max, "gte": cadd_min}) | ~EQ("exists", field='cadd'))


def filter_by_mcap(request, args, args_es):
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
            args_es.append(EQ("range", mcap_score={"lte": mcap_max, "gte": mcap_min}))
        else:
            args.append((Q(mcap_score__lte=mcap_max) & Q(mcap_score__gte=mcap_min)) | Q(mcap_score__isnull=True))
            args_es.append(
                EQ("range", mcap_score={"lte": mcap_max, "gte": mcap_min}) | ~EQ("exists", field='mcap_score'))


def filter_by_rf_score(request, args, args_es):
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
            args_es.append(EQ("range", rf_score={"lte": rf_max, "gte": rf_min}))
        else:
            args.append((Q(rf_score__lte=rf_max) & Q(rf_score__gte=rf_min)) | Q(rf_score__isnull=True))
            args_es.append(EQ("range", rf_score={"lte": rf_max, "gte": rf_min}) | ~EQ("exists", field='rf_score'))


def filter_by_ada_score(request, args, args_es):
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
            args_es.append(EQ("range", ada_score={"lte": ada_max, "gte": ada_min}))
        else:
            args.append((Q(ada_score__lte=ada_max) & Q(ada_score__gte=ada_min)) | Q(ada_score__isnull=True))
            args_es.append(EQ("range", ada_score={"lte": ada_max, "gte": ada_min}) | ~EQ("exists", field='ada_score'))


def filter_by_pp2(request, args, args_es):
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
            args_es.append(EQ("range", polyphen2={"lte": polyphen_max, "gte": polyphen_min}))
        else:
            args.append((Q(polyphen2__lte=polyphen_max) & Q(polyphen2__gte=polyphen_min)) | Q(polyphen2__isnull=True))
            args_es.append(
                EQ("range", polyphen2={"lte": polyphen_max, "gte": polyphen_min}) | ~EQ("exists", field='polyphen2'))


def filter_by_segdup(request, args):
    # ToDo: this is being used?
    exclude_segdup = request.GET.get('exclude_segdup', '')
    if exclude_segdup == 'on':
        args.append(Q(segdup=''))


def filter_cgd(request, args, args_es):
    cgdmanifestation = request.GET.getlist('cgdmanifestation')
    # interventions = request.GET.getlist('interventions')
    conditions = request.GET.getlist('cgd')
    if len(cgdmanifestation) > 0:
        if cgdmanifestation[0] != '':
            # get a list of CGDENTRY
            cgdentries = CGDEntry.objects.filter(MANIFESTATION_CATEGORIES__in=cgdmanifestation)
            gene_list = []
            for gene in cgdentries:
                gene_list.append(gene.GENE)
            args.append(Q(gene__in=gene_list))
            args_es.append(EQ("match", gene=str(gene_list)))
    if len(conditions) > 0:
        if conditions[0] != '':
            cgdentries = CGDEntry.objects.filter(CONDITIONS__in=conditions)
            gene_list = []
            for gene in cgdentries:
                gene_list.append(gene.GENE)
            args.append(Q(gene__in=gene_list))
            args_es.append(EQ("match", gene=str(gene_list)))


def filter_omim(request, args, args_es):
    omim = request.GET.getlist('omim')
    print('omim', omim)
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
            should_list = [EQ("match_phrase", gene=gene_) for gene_ in gene_list]
            args_es.append(EQ('bool', should=should_list, minimum_should_match=1))


def filter_hgmd(request, args, args_es):
    hgmd = request.GET.getlist('hgmd')
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
            should_list = [EQ("match_phrase", gene=gene_) for gene_ in gene_list]
            args_es.append(EQ('bool', should=should_list, minimum_should_match=1))


def filter_genelists(request, query, args, exclude, args_es):
    genelists = request.GET.getlist('genelists')

    safe_gene_list = []
    if len(genelists) > 0:

        for genelist_id in genelists:
            genelist_obj = GeneList.objects.get(pk=genelist_id)
            gene_list = genelist_obj.genes.split(',')
            for gene in gene_list:
                if gene not in safe_gene_list:
                    safe_gene_list.append(gene.upper())
        query['gene__in'] = safe_gene_list
        should_list = [EQ("match_phrase", gene=gene_) for gene_ in safe_gene_list]
        args_es.append(EQ('bool', should=should_list, minimum_should_match=1))

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
            should_list = [EQ("match_phrase", gene=gene_) for gene_ in exclude_safe_gene_list]
            args_es.append(~EQ('bool', should=should_list, minimum_should_match=1))


# HERE STARTS FILTER FOR FAMILY ANALYSIS
def filter_inheritance_option(request):
    inheritance_option = request.GET.get('inheritance_option', '')

    if inheritance_option == '3':
        request.GET.__setitem__('variants_per_gene', '2')
        request.GET.__setitem__('variants_per_gene_option', '>')
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


def filter_inheritance_option_mutation_type(request, args, args_es):
    inheritance_option = request.GET.get('inheritance_option', '')
    # by exclusion of genotypes
    if inheritance_option == '1':
        genotypes = ['0/0', './.', '0/1', '1/0', '0/2', '2/0']
        args.append(~Q(genotype__in=genotypes))
        should_list = [Q("match_phrase", genotype=genotype) for genotype in genotypes]
        args_es.append(EQ('bool', should=should_list, minimum_should_match=1))


def filter_sift(request, args, args_es):
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
                args_es.append(EQ("range", sift={"lte": float(sift)}))
            else:
                args.append(Q(sift__lte=float(sift)) | Q(sift__isnull=True))
                args_es.append(EQ("range", sift={"lte": float(sift)}) | ~EQ("exists", field='sift'))
        elif sift_option == '>':
            if sift_flag:
                args.append(Q(sift__gte=float(sift)))
                args_es.append(EQ("range", sift={"gte": float(sift)}))
            else:
                args.append(Q(sift__gte=float(sift)) | Q(sift__isnull=True))
                args_es.append(EQ("range", sift={"gte": float(sift)}) | ~EQ("exists", field='sift'))
        elif sift_option == '=':
            if sift_flag:
                args.append(Q(sift=float(sift)))
                args_es.append(EQ("match", sift=float(sift)))
            else:
                args.append(Q(sift=float(sift)) | Q(sift__isnull=True))
                args_es.append(EQ("match", sift=float(sift)) | ~EQ("exists", field='sift'))


def filter_polyphen2(request, args, args_es):
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
                args_es.append(EQ("range", polyphen2={"lte": float(polyphen)}))
            else:
                args.append(Q(polyphen2__lte=float(polyphen)) | Q(polyphen2__isnull=True))
                args_es.append(EQ("range", polyphen2={"lte": float(polyphen)}) | ~EQ("exists", field='polyphen2'))
        elif polyphen_option == '>':
            if polyphen_flag:
                args.append(Q(polyphen2__gte=float(polyphen)))
                args_es.append(EQ("range", polyphen2={"gte": float(polyphen)}))
            else:
                args.append(Q(polyphen2__gte=float(polyphen)) | Q(polyphen2__isnull=True))
                args_es.append(EQ("range", polyphen2={"gte": float(polyphen)}) | ~EQ("exists", field='polyphen2'))
        elif polyphen_option == '=':
            if polyphen_flag:
                args.append(Q(polyphen2=float(polyphen)))
                args_es.append(EQ("match", polyphen2=float(polyphen)))
            else:
                args.append(Q(polyphen2=float(polyphen)) | Q(polyphen2__isnull=True))
                args_es.append(EQ("match", polyphen2=float(polyphen)) | ~EQ("exists", field='polyphen2'))


def filter_dbsnp_build(request, args, args_es):
    dbsnp_build = request.GET.get('dbsnp_build', '')
    if dbsnp_build != '':
        dbsnp_option = request.GET.get('dbsnp_option', '')
        if dbsnp_option == '<':
            # build_list = range(1, int(dbsnp_build))
            # T2 = [str(x) for x in build_list]
            # T2.append('')
            # query['dbsnp_build__in'] = #T2
            args.append(Q(dbsnp_build__lte=int(dbsnp_build)) | Q(dbsnp_build__isnull=True))
            args_es.append(EQ("range", dbsnp_build={"lte": int(dbsnp_build)}) | ~EQ("exists", field='dbsnp_build'))
        elif dbsnp_option == '>':
            # build_list = range(int(dbsnp_build), 138)
            # T2 = [str(x) for x in build_list]
            # T2.append('')
            # query['dbsnp_build__in'] = T2
            args.append(Q(dbsnp_build__gte=int(dbsnp_build)) | Q(dbsnp_build__isnull=True))
            args_es.append(EQ("range", dbsnp_build={"gte": int(dbsnp_build)}) | ~EQ("exists", field='dbsnp_build'))


def filter_read_depth(request, args, args_es):
    read_depth = request.GET.get('read_depth', '')
    if read_depth != '':
        read_depth_option = request.GET.get('read_depth_option', '')
        if read_depth_option == '<':
            args.append(Q(read_depth__lte=int(read_depth)))
            args_es.append(EQ("range", read_depth={"lte": int(read_depth)}))
        elif read_depth_option == '>':
            args.append(Q(read_depth__gte=int(read_depth)))
            args_es.append(EQ("range", read_depth={"gte": int(read_depth)}))
        elif read_depth_option == '=':
            args.append(Q(read_depth=int(read_depth)))
            args_es.append(EQ("match", read_depth=int(read_depth)))


def filter_func_class(request, query, args_es):
    func_class = request.GET.getlist('func_class')
    if len(func_class) > 0:
        query['snpeff_func_class__in'] = func_class
        should_list = [EQ("match_phrase", snpeff_func_class=func_) for func_ in func_class]
        args_es.append(EQ('bool', should=should_list, minimum_should_match=1))


def filter_impact(request, query, args_es):
    impact = request.GET.getlist('impact')
    if len(impact) > 0:
        # query['snpeff__impact__in'] = impact
        query['snpeff_impact__in'] = impact
        should_list = [EQ("match_phrase", snpeff_impact=impact_) for impact_ in impact]
        args_es.append(EQ('bool', should=should_list, minimum_should_match=1))


def filter_is_at_hgmd(request, query, args_es):
    # hgmd = request.GET.getlist('is_at_hgmd')
    hgmd = request.GET.get('is_at_hgmd', '')
    if hgmd == 'on':
        query['is_at_hgmd'] = True
        args_es.append(EQ("match", is_at_hgmd=True))


def filter_clnsig(request, query, args_es):
    # hgmd = request.GET.getlist('is_at_hgmd')
    clnsig = request.GET.get('clnsig', '')
    if clnsig != '':
        query['clinvar_clnsig'] = clnsig
        args_es.append(EQ("match", clinvar_clnsig=clnsig))


def export_to_csv(request, variants):
    # export to csv
    export = request.GET.get('export', '')
    if export != '':
        content_type = 'text/plain'
        content_disposition = 'attachment; filename=export.txt'
        writer_kwargs = {}
        if export == 'csv':
            content_type = 'text/csv'
            content_disposition = 'attachment; filename=export.csv'
        elif export == 'txt':
            writer_kwargs = {
                'delimiter': '\t',
                'quoting': csv.QUOTE_NONE
            }
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = content_disposition
        writer = csv.writer(response, **writer_kwargs)

        writer.writerow(['Individual', 'Index', 'Pos_index', 'Chr', 'Pos', 'Variant_id', 'Ref', 'Alt', 'Qual', 'Filter',
                         'Info', 'Format', 'Genotype_col', 'Genotype', 'Read_depth', 'Gene', 'Mutation_type', 'Vartype',
                         'Genomes1k_maf', 'Dbsnp_maf', 'Esp_maf', 'Dbsnp_build', 'Sift', 'Sift_pred', 'Polyphen2',
                         'Polyphen2_pred', 'Condel', 'Condel_pred', 'DANN', 'CADD', 'Is_at_omim', 'Is_at_hgmd',
                         'Hgmd_entries', 'Effect', 'Impact', 'Func_class', 'Codon_change', 'Aa_change', 'Aa_len',
                         'Gene_name', 'Biotype', 'Gene_coding', 'Transcript_id', 'Exon_rank', 'Genotype_number',
                         'Allele', 'Gene', 'Feature', 'Feature_type', 'Consequence', 'Cdna_position', 'Cds_position',
                         'Protein_position', 'Amino_acids', 'Codons', 'Existing_variation', 'Distance', 'Strand',
                         'Symbol', 'Symbol_source', 'Sift', 'Polyphen', 'Condel'])
        for variant in variants:
            # print 'variant', variant.index
            writer.writerow([variant.individual, variant.index, variant.pos_index, variant.chr, variant.pos,
                             variant.variant_id, variant.ref, variant.alt, variant.qual, variant.filter,
                             pickle.loads(variant.info), variant.format, variant.genotype_col, variant.genotype,
                             variant.read_depth, variant.gene, variant.mutation_type, variant.vartype,
                             variant.genomes1k_maf, variant.dbsnp_maf, variant.esp_maf, variant.dbsnp_build,
                             variant.sift, variant.sift_pred, variant.polyphen2, variant.polyphen2_pred, variant.condel,
                             variant.condel_pred, variant.dann, variant.cadd, variant.is_at_omim, variant.is_at_hgmd,
                             variant.hgmd_entries])
        return response
