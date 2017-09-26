# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Min, Max
from django.views.generic import ListView, DetailView
from django.contrib.admin.views.decorators import staff_member_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.views.generic.detail import DetailView

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
from diseases.models import *
from individuals.models import *
from variants.models import *
import codecs
from django.db.models import Q
#from mysql_bulk_insert import bulk_insert
import re
from .forms import *
from collections import Counter
#import settings
# from goatools import obo_parser
from genes.models import *
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.http import Http404
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render


def genesetcreate(request):
    form = GenesetForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
            genelist = GeneList()
            genelist.name = form.cleaned_data['name'] 


            genelist_list = form.cleaned_data['genes']

            genelist_list = genelist_list.split('\r\n')
            # print 'gene_list'
            if genelist_list[0] != '':
                safe_gene_list = []
                for row in genelist_list:
                    row = row.split(',')
                    for item in row:
                        gene = item.strip()
                        if (gene != ' ' and gene != ''):
                            if gene not in safe_gene_list:
                                safe_gene_list.append(item.strip())

            genelist.genes = ",".join(safe_gene_list)
            #form.cleaned_data['genes']



            genelist.user=request.user
            genelist.save()
            # form.save()

            
            
            return redirect(reverse('genes_list'))

    # context = RequestContext(request, )
    return render(request, 'genes/genelist_create.html', {'form': form})



class GenesetDetailView(DetailView):
    model = GeneList
    context_object_name = "geneset"

    def get_template_names(self):
        return ["genes/genelist_detail.html"]

    def get_object(self):
        #get objects
        return GeneList.objects.filter(id=self.kwargs['pk'])[0]


    def get_context_data(self, **kwargs):
        context = super(GenesetDetailView, self).get_context_data(**kwargs)
        return context

# class GenesetDeleteView(DeleteView):
#     def get_object(self, queryset=None):
#         """ Hook to ensure object is owned by request.user. """
#         obj = super(GenesetDeleteView, self).get_object()
#         if not obj.owner == self.request.user:
#             raise Http404
#         return obj

def delete_genelist(request,pk):
    u = GeneList.objects.filter(id=pk)[0]
    
    if u.user == request.user:
        u.delete()
    
    return redirect(reverse('genes_list'))


class ListGene(ListView):
    model = Gene      #implies -> queryset = models.Car.objects.all()
    paginate_by = 100  #and that's it !!
    context_object_name = "genes"
    
    def get_queryset(self, **kwargs):
        q = self.request.GET.get('q', '')
        return Gene.objects.filter(Q(name__icontains=q)|Q(symbol__icontains=q))

    def post(self, request, *args, **kwargs):
        #get list of diseases
        genes_ids = request.POST.getlist('genes')
        genes = Gene.objects.filter(id__in=genes_ids)
        #create list of genes
        gene_list = []
        for gene in genes:
            gene_list.append(gene.symbol)
        #redirect to filter analysis page
        return redirect('/filter_analysis/?gene_list=%s' % ("%2C".join(gene_list)))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListGene, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['genelists'] = GeneList.objects.all().order_by('name')

        return context

class GeneDetail(DetailView):
    model = Gene
    


# @login_required
# def populate_termsfromgo(request):
#     p = obo_parser.GODag('data/gene_ontology.1_2.obo')
#     goterms = []
#     goterms_dict = []
#     goterms_parents_children = {}
    
#     #print p["GO:0022610"]
#     #print p["GO:0022610"].parents
#     #print p["GO:0022610"].children
    
#     for item in p:
#       if p[item].id not in goterms_dict:
# 	goterms_dict.append(p[item].id)
# 	goterm = GoTerm(goid=p[item].id,
# 		      name=p[item].name,
# 		      namespace=p[item].namespace,
# 		      level=p[item].level,
# 		      is_obsolete=p[item].is_obsolete,
# 		      alt_ids=p[item].alt_ids
# 	)
	
	
# 	goterms_parents_children[p[item].id] = {}
# 	#print p[item]
# 	goterms_parents_children[p[item].id]['parents'] = []
# 	#print 'parents'
# 	for parent in p[item].parents:
# 	  #print parent
# 	  goterms_parents_children[p[item].id]['parents'].append(parent.id)
	
	
# 	goterms_parents_children[p[item].id]['children'] = []
# 	#print 'children'
# 	for child in p[item].children:
# 	  #print child
# 	  goterms_parents_children[p[item].id]['children'].append(child.id)
	
# 	goterms.append(goterm)
	      
#     GoTerm.objects.bulk_create(goterms)
#     print 'finished inserting files'
#     goterms = GoTerm.objects.all()
#     goterms_dict = {}
#     for goterm in goterms:
#       goterms_dict[goterm.goid] = goterm
      
#     print 'finished creating dict'
    
#     with transaction.commit_on_success():
      
#       for goid in goterms_parents_children:
# 	#get goterm
# 	goterm = goterms_dict[goid]
# 	#for each parent
# 	for parentgoid in goterms_parents_children[goid]['parents']:
# 	  goterm.parents.add(goterms_dict[parentgoid])
	
	
# 	#add children
# 	for childrengoid in goterms_parents_children[goid]['children']:
# 	  goterm.children.add(goterms_dict[childrengoid])
	
	
      
#       #add parents
#       #add children
	
#     #open file with GO's
#     print 'finish filling Terms from Go'
#     messages.add_message(request, messages.INFO, "Finish filling Terms from Go")
#     return redirect('/databases/')


@login_required
def populate_fromgo(request):
    #open file with GO's
    gofile = open('data/go_gene_terms')
    
    genes = {}
    gos = {}
    relationships = {}
    
    count_line = 0
    count2 = 0
    for line in gofile:
      #get line
      count_line += 1
      count2 += 1
      if count2 == 5000:
        print(count_line)
        count2 = 0
      line = line.split('\t')
      #GO
      go =  line[0]
      domain = line[1]
      category_name = line[2]
      definition = "\"".join(line[3].split('"')[1:-1])
      #Gene
      gene_symbol = line[4].upper()
      gene_description = line[5]
      
      if gene_symbol not in genes:
        gene = Gene(symbol=gene_symbol, description = gene_description)
        genes[gene_symbol] = gene
      else:
        gene = genes[gene_symbol] 

      if go not in gos:
        genecategory = GeneCategory(go=go, name=category_name, domain=domain)
        gos[go] = genecategory
      else:
        genecategory = gos[go]
      
      #add relationships
      if go not in relationships:
        relationships[go] = []
      if gene_symbol not in relationships[go]:
        relationships[go].append(gene_symbol)
      
    
    Gene.objects.bulk_create(list(genes.values()))
    GeneCategory.objects.bulk_create(list(gos.values()))
    print('Creating relationships')
    
    genes = Gene.objects.all()
    genes_dict = {}
    for gene in genes:
      genes_dict[gene.symbol] = gene
    
    
    gene_categories = GeneCategory.objects.all()
    categories_dict = {}
    for category in gene_categories:
      categories_dict[category.go] = category
    print('finished creating dicts')
    
    #RelationShips
    memberships = []
    count_membership = 0
    count_membership2 = 0
    for go in relationships:
      #gene_category = GeneCategory.objects.get(go=go)
      
      for gene_symbol in relationships[go]:
        count_membership += 1
        count_membership2 += 1
    if count_membership2 == 5000:
      print(count_membership)
      Membership.objects.bulk_create(memberships)
      memberships = []
      count_membership2 = 0
      
    #get gene
    #gene = Gene.objects.get(symbol=gene_symbol)
    membership = Membership(gene=genes_dict[gene_symbol], group=categories_dict[go])
    memberships.append(membership)
    #relationship_list.append(relationship)
    
    Membership.objects.bulk_create(memberships)
    print('finish filling genes from Go')
    messages.add_message(request, messages.INFO, "Finished filling genes from GO")
    return redirect('/databases/')
    
    
# Create your views here.
@login_required
def populate(request):
    
    hgnc = codecs.open('data/hgnc/hgnc_downloads.cgi.txt', 'r', "ISO-8859-1")
    header = hgnc.readline().strip().split('\t')
    count_gene = 1
    
    genes = []
    countline = 0
    for line in hgnc:
#        print count_gene

        count_gene += 1
        countline += 1
        #print countline
        if count_gene == 5000:
            print(countline)
            #bulk_insert(genes, show_sql=False)
            Gene.objects.bulk_create(genes)
            count_gene = 0
            genes = []
        
#        print line
        line = line.strip().split('\t')
#        print len(line)
#        print line
        #ugly hack
        if len(line) != 41:
            count = 41 - len(line) 
            for item in range(0,count):
                line.append('')
        
        gene = Gene(symbol = line[1],
                    name = line[2],
                    locus_type = line[4],
                    locus_group = line[5],
                    previous_symbols = line[6],
                    previous_names = line[7],
                    synonyms = line[8],
                    name_synonyms = line[9],
                    chromossome = line[10],
                    date_approved = line[11],
                    date_modified = line[12],
                    date_symbol_changes = line[13],
                    date_name_changes = line[14],
                    accesion_numbers = line[15],
                    enzyme_ids = line[16],
                    entrez_gene_id = line[17],
                    emsembl_gene_id = line[18],
                    mouse_genome_database_id = line[19],
                    specialist_database_links = line[20],
                    specialist_database_ids = line[21],
                    pubmed_ids = line[22],
                    refseq_ids = line[23],
                    gene_famili_tag = line[24],
                    gene_family_description = line[25],
                    record_type = line[26],
                    primary_ids = line[27],
                    secondary_ids = line[28],
                    ccds_ids = line[29],
                    vega_ids = line[30],
                    locus_specific_databases = line[31],
                    gdb_id_mapped = line[32],
                    entrez_gene_id_mapped = line[33],
                    omim_id = line[34],
                    refseq_id = line[35],
                    uniprot_id = line[36],
                    ensembl_id = line[37],
                    ucsc_id = line[38],
                    mouse_genome_database = line[39],
                    rat_genome_database = line[40])
    
        
        genes.append(gene)

    Gene.objects.bulk_create(genes)
    #bulk_insert(genes, show_sql=False)
    hgnc.close()
    print('finish filling genes')
    messages.add_message(request, messages.INFO, "Finished filling genes")
    return redirect('/databases/')


@login_required
def view(request, gene_name):
#    gene = Variant.objects.filter(gene_name=gene_name).annotate(num_individuals=Count('individuals'))
    gene_object = Gene.objects.get(symbol=gene_name)
    
    #get all variants present in this gene
    gene_variants = Variant.objects.filter(gene=gene_name)
    
    #variants by individuals
    variants_by_individuals = gene_variants.values('individual').annotate(total=Count('individual')).order_by('individual')
    
    #put all summary in this variable
    variants_summary = {}
    variants_summary['individual'] = {'known':0, 'novel':0, 'total':0} 
    for individual in variants_by_individuals:
        individual['individual'] = get_object_or_404(Individual, pk=individual['individual'])
        individual['novel'] = Variant.objects.filter(gene=gene_name, individual=individual['individual'], variant_id='.').count()
        individual['known'] = individual['total'] - individual['novel']
        
        #update total summary
        variants_summary['individual']['known'] += individual['known'] 
        variants_summary['individual']['novel'] += individual['novel']
        variants_summary['individual']['total'] += individual['total']
    
    
    
    #by effect and by individual
    #this is summary for snp_eff already (not by individual, only snp_eff)
    dna_variation = gene_variants.values('snpeff_effect').annotate(total=Count('snpeff_effect')).order_by('snpeff_effect')
    dna_variation_classes = dna_variation.values_list('snpeff_effect', flat=True)
    individuals_dna_variation = {}
    #for each individual
    for individual in variants_by_individuals:
        individual_dna_variation = {}
        #get all variants from individual by effect
        variants = Variant.objects.filter(gene=gene_name, individual=individual['individual']).values('snpeff_effect').annotate(total=Count('snpeff_effect')).order_by('snpeff_effect')
        for item in variants:
            individual_dna_variation[item['snpeff_effect']] = item['total'] 
        individuals_dna_variation[individual['individual']] = individual_dna_variation
    #print individuals_dna_variation
    
    
    functional_class = Variant.objects.filter(gene=gene_name).values('snpeff_func_class').annotate(total=Count('snpeff_func_class')).order_by('snpeff_func_class')
    
    functional_class_classes = functional_class.values_list('snpeff_func_class', flat=True)
    
    individuals_functional_class = {}
    for individual in variants_by_individuals:
        individual_functional_class = {}
        variants = Variant.objects.filter(gene=gene_name, individual=individual['individual']).values('snpeff_func_class').annotate(total=Count('snpeff_func_class')).order_by('snpeff_func_class')
        for item in variants:
            individual_functional_class[item['snpeff_func_class']] = item['total'] 
        individuals_functional_class[individual['individual']] = individual_functional_class
        
    
    impact = Variant.objects.filter(gene=gene_name).values('snpeff_impact').annotate(total=Count('snpeff_impact')).order_by('snpeff_impact')
    print(impact) 
    impact_classes = impact.values_list('snpeff_impact', flat=True)
    individuals_impact = {}
    for individual in variants_by_individuals:
        individual_impact = {}
        variants = Variant.objects.filter(gene=gene_name, individual=individual['individual']).values('snpeff_impact').annotate(total=Count('snpeff_impact')).order_by('snpeff_impact')
        for item in variants:
            individual_impact[item['snpeff_impact']] = item['total'] 
        individuals_impact[individual['individual']] = individual_impact
#    dna_variation = Variant.objects.filter(gene_name=gene_name).values_list('snp_eff').annotate(total=Count('snp_eff')).order_by('snp_eff')
#    functional_class = Variant.objects.filter(gene_name=gene_name).values_list('snp_eff_functional_class').annotate(total=Count('snp_eff_functional_class')).order_by('snp_eff_functional_class')
#    protein_impact = Variant.objects.filter(gene_name=gene_name).values_list('impact').annotate(total=Count('impact')).order_by('impact')
#    print gene.count()
    
    return render(request, 'genes/view.html', {'gene_object':gene_object,
                                                  'variants_by_individuals': variants_by_individuals,
                                                  'variants_summary':variants_summary,
                                                  'dna_variation':dna_variation, 
                                                  'dna_variation_classes':dna_variation_classes,
                                                  'individuals_dna_variation':individuals_dna_variation,
                                                  'functional_class':functional_class,
                                                  'functional_class_classes':functional_class_classes,
                                                  'individuals_functional_class':individuals_functional_class,
                                                  'impact':impact,
                                                  'impact_classes':impact_classes,
                                                  'individuals_impact':individuals_impact})



@login_required
def creategroup(request):
    if request.method == 'POST':
        form = GeneGroupForm(request.POST)        
        if form.is_valid():
            
            #use id for unique names
            genegroup = GeneGroup.objects.create(
                                                 name=form.cleaned_data['name'], 
                                                 genes=form.cleaned_data['genes'])
            genegroup.save()
            return HttpResponseRedirect('/filteranalysis/')
    else:
        form = GeneGroupForm()
    return render(request, 'genes/creategenegroup.html', {'form': form})

    
@login_required
def geneontology(request, go_id=''):
    #print go_id
    #if go_id != '':
      #goterms = GoTerm.objects.get(goid=go_id)
      ##GO:0003674 # molecular function
      ##GO:0005575 # celular component
      ##GO:0008150 # biological process
    
    go_ids = ['GO:0003674', 'GO:0005575', 'GO:0008150']
    goterms = GoTerm.objects.filter(goid__in = go_ids).order_by('name')
    
    return render(request, 'genes/geneontology.html', {'goterms':goterms})

    
def get_all_children(goterm):
    yield goterm.goid
#    lista = [goterm.goid]
    if goterm.children.all() != []:
        for child in goterm.children.all():
            yield child.goid
#            lista = lista + get_all_children(child)
#    return lista
    
  
    
@login_required
def geneontology_view(request, go_id=''):
#    print go_id
    if go_id != '':
      goterm = GoTerm.objects.get(goid=go_id)
      children = goterm.children.order_by('name')
      parents = goterm.parents.order_by('name')
    #get all children
    #print children
    
    all_children = [x for x in get_all_children(goterm)]
#    print all_children
#    
##    print all_children
##    for goterm_child in all_children:
##        print goterm_child 
#    
#    #test = GoTerm.objects.filter(id=goterm.id).prefetch_related('children')
#    #print test
    genes_categories = GeneCategory.objects.filter(go__in=all_children).values_list('id', flat=True)
    genes = Membership.objects.filter(group__in=genes_categories)
#    
#    genes = [] 
    
    paginator = Paginator(genes, 100) # Show 25 contacts per page
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        genes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        genes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        genes = paginator.page(paginator.num_pages)
	
      
      
      
    print(len(genes))  
    
    
    return render(request, 'genes/geneontology_view.html', {'goterm':goterm, 'children':children, 'parents':parents, 'genes':genes})


@staff_member_required
def populate_cgd(request):
    CDGfile = open('data/CGD/CGD.txt')
    header = next(CDGfile)
    for line in CDGfile:
        gene_item = line.split('\t')
        # print gene_item
        cgd = CGDEntry()

        cgd.GENE = gene_item[0]
        cgd.ENTREZ_GENE_ID = gene_item[1]
        
        cgd.INHERITANCE = gene_item[3]
        cgd.AGE_GROUP = gene_item[4]
        cgd.ALLELIC_CONDITIONS = gene_item[5]

        cgd.COMMENTS = gene_item[8]
        cgd.INTERVENTION_RATIONALE = gene_item[9]
        
        references_list =[]
        references = gene_item[10].split(';')
        for ref in references:
            references_list.append(ref.strip())

        cgd.REFERENCES = references_list

        cgd.save()
        
        manifestations = gene_item[6].split(';')
        for manifestation in  manifestations:
            #try get manifestation
            manifestation = manifestation.strip()
            if manifestation != '':
                man_obj = Manifestation.objects.get_or_create(name=manifestation)[0]
                cgd.MANIFESTATION_CATEGORIES.add(man_obj)
                # cgd.MANIFESTATION_CATEGORIES.append(man_obj)  
                

        interventions = gene_item[7].split(';')
        for intervention in  interventions:
            #try get manifestation
            intervention = intervention.strip()
            int_obj = Intervention.objects.get_or_create(name=intervention)[0]
            cgd.INTERVENTION_CATEGORIES.add(int_obj)
            # cgd.INTERVENTION_CATEGORIES.append(int_obj)

        conditions = gene_item[2].split(';')
        for condition in conditions:
            condition = condition.strip()
            if condition != '':
                cond_obj = CGDCondition.objects.get_or_create(name=condition)[0]
                cgd.CONDITIONS.add(cond_obj)
                # cgd.CONDITIONS.append(cond_obj)

        

    return redirect('/genes')


@staff_member_required
def create_cgd_categories(request):
    #get categories
    manifestations = Manifestation.objects.all()
    recessive = open('%s/data/lupski/Lupski genes recessivos.txt' % (settings.BASE_DIR))
    recessive_gene_list = []
    for line in recessive:
        genes = line.split(',')
        for gene in genes:
            recessive_gene_list.append(gene.strip().upper())
    
    genelist = GeneList()
    genelist.name = 'Lupski recessive genes'
    genelist.genes = ",".join(recessive_gene_list)
    genelist.user=request.user
    genelist.save()

    dominant = open('%s/data/lupski/Lupski genes dominantes.txt' % (settings.BASE_DIR))
    dominant_gene_list = []
    for line in dominant:
        genes = line.split(',')
        for gene in genes:
            dominant_gene_list.append(gene.strip().upper())

    genelist = GeneList()
    genelist.name = 'Lupski dominant genes'
    genelist.genes = ",".join(recessive_gene_list)
    genelist.user=request.user
    genelist.save()

    xlinked = Disease.objects.filter(name__icontains="X-Linked")
    # print xlinked
    xlinked_gene_list = []
    for disease in xlinked:
        genes = disease.gene_names.split(',')
        for gene in genes:
            xlinked_gene_list.append(gene.strip())
    # xlinked_gene_list

    for manifestation in manifestations:
        
        # print manifestation

        #get genes from this manifestation
        cgdentries = CGDEntry.objects.filter(MANIFESTATION_CATEGORIES__in=[manifestation])
        gene_list = []
        for gene in cgdentries:
           gene_list.append(gene.GENE)

        #intersect with recessive
        intersection_lists = []
        intersection_lists.append(set(recessive_gene_list))
        intersection_lists.append(set(gene_list))
        genes_in_common_list = set.intersection(*intersection_lists)
        
        #create gene list
        genelist = GeneList()
        genelist.name = '%s_manifestation_recessive' % (manifestation)
        genelist.genes = ",".join(genes_in_common_list)
        genelist.user=request.user
        genelist.save()

        #intersect with dominant
        intersection_lists = []
        intersection_lists.append(set(dominant_gene_list))
        intersection_lists.append(set(gene_list))
        genes_in_common_list = set.intersection(*intersection_lists)
        
        #create gene list
        genelist = GeneList()
        genelist.name = '%s_manifestation_dominant' % (manifestation)
        genelist.genes = ",".join(genes_in_common_list)
        genelist.user=request.user
        genelist.save()

        #intersect with xlinked
        intersection_lists = []
        intersection_lists.append(set(xlinked_gene_list))
        intersection_lists.append(set(gene_list))
        genes_in_common_list = set.intersection(*intersection_lists)
        
        #create gene list
        genelist = GeneList()
        genelist.name = '%s_manifestation_xlinked' % (manifestation)
        genelist.genes = ",".join(genes_in_common_list)
        genelist.user=request.user
        genelist.save()

    return redirect(reverse('databases_index'))

