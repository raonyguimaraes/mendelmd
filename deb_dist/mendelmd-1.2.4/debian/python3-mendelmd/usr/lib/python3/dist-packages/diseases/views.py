# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
from django.contrib import messages
from individuals.models import Individual
from variants.models import Variant

from diseases.models import *
from genes.models import Gene as Gene2
from django.db.models import Q

# import urllib.request, urllib.parse, urllib.error

from django.views.generic import ListView
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
# from bs4 import BeautifulSoup
# import bs4
import os


#class based
#@login_required
class DiseaseListView(ListView):
    model = Disease      #implies -> queryset = models.Car.objects.all()
    paginate_by = 100  #and that's it !!
    context_object_name = "diseases"
    
    def get_queryset(self, **kwargs):
        name = self.request.GET.get('name', '')    
        return Disease.objects.filter(Q(name__icontains=name)|Q(gene_names__icontains=name))

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(DiseaseListView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DiseaseListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        diseases = context['object_list']
        gene_list = []
        for disease in diseases:
            genes = disease.gene_names.split(',')
            for gene in genes:
                gene_list.append(gene.strip())
        context['filter_query'] = "%2C".join(gene_list)
        return context
    
    def post(self, request, *args, **kwargs):
        #get list of diseases
        diseases_ids = request.POST.getlist('diseases')
        diseases = Disease.objects.filter(id__in=diseases_ids)
        #create list of genes
        gene_list = []
        for disease in diseases:
            genes = disease.gene_names.split(',')
            for gene in genes:
                parsed_gene = gene.strip()
                if parsed_gene not in gene_list:
                    gene_list.append(parsed_gene)
        #redirect to filter analysis page
        gene_list_url = '?gene_list=%s' % ("%2C".join(gene_list))
        #return redirect('/filter_analysis/?gene_list=%s' % ("%2C".join(gene_list)))
        # return redirect(reverse('filter_analysis', args=['some_value']))
        return redirect(reverse('filter_analysis')+gene_list_url)
        # return redirect('filter_analysis', gene_list='%s' % ("%2C".join(gene_list)))

class HGMDGeneListView(ListView):
    model = HGMDGene      #implies -> queryset = models.Car.objects.all()
    paginate_by = 100  #and that's it !!
    context_object_name = "genes"
    
    def get_queryset(self, **kwargs):
        name = self.request.GET.get('name', '')    
        return HGMDGene.objects.filter(Q(name__icontains=name)|Q(gene_names__icontains=name))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HGMDGeneListView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HGMDGeneListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        genes = context['object_list']
        # gene_list = []
        # for disease in diseases:
        #     genes = disease.gene_names.split(',')
        #     for gene in genes:
        #         gene_list.append(gene.strip())
        # context['filter_query'] = "%2C".join(gene_list)
        return context
    
    def post(self, request, *args, **kwargs):
        #get list of diseases
        diseases_ids = request.POST.getlist('diseases')
        diseases = Disease.objects.filter(id__in=diseases_ids)
        #create list of genes
        gene_list = []
        for disease in diseases:
            genes = disease.gene_names.split(',')
            for gene in genes:
                gene_list.append(gene.strip())
        #redirect to filter analysis page
        gene_list_url = '?gene_list=%s' % ("%2C".join(gene_list))
        #return redirect('/filter_analysis/?gene_list=%s' % ("%2C".join(gene_list)))
        # return redirect(reverse('filter_analysis', args=['some_value']))
        return redirect(reverse('filter_analysis')+gene_list_url)
        # return redirect('filter_analysis', gene_list='%s' % ("%2C".join(gene_list)))
                

import os
@staff_member_required
def populate(request):

    print(os.getcwd())
    
    morbidmap = open('data/omim/morbidmap', 'r')
    for line in morbidmap:
#        print line
        line = line.strip().split('|')
        name = line[0]
        omim_id = line[2]
        chr_location = line[3]
        gene_names = line[1]
        disease = Disease.objects.create(name=name, omim_id=omim_id, chr_location=chr_location, gene_names=gene_names)
        disease.save()
        genes = line[1].split(',')
        
        
        gene_officialname = genes[0].strip()
        
        chr_candidate = line[3].split('q')[0]
        chr_candidate2 = line[3].split('p')[0]
        if len(chr_candidate) < len(chr_candidate2):
            chromossome = chr_candidate
        else:
            chromossome = chr_candidate2
        #add gene relation with disease
        if gene_names != '':
            #check if gene exists otherwise create gene
            try:
                gene = Gene.objects.get(names=gene_names, official_name=gene_officialname, chromossome=chromossome)
                gene.diseases.add(disease)
                gene.save()
            except Gene.DoesNotExist:
                gene = Gene.objects.create(names=gene_names, official_name=gene_officialname, chromossome=chromossome)
                gene.save()
                gene.diseases.add(disease)
                gene.save()
                
         
            #same for genes_Gene
            #check if gene exists for each alternative name of gene
            gene_names = gene_names.strip().split(',')
            try:
                gene = Gene2.objects.get(symbol=gene_officialname)
                gene.diseases.add(disease)
                gene.save()
            except Gene2.DoesNotExist:
                print('gene symbol doesnt exists in HGNC')
                print(gene_officialname)
                print(gene_names)
#   for gene_symbol in gene_names:
#       

        
        
                    #gene = Genes_Gene.objects.create(names=gene_names, official_name=gene_officialname, chromossome=chromossome)
                    #gene.save()
                    #gene.diseases.add(disease)
                    #gene.save()
                    
                 
                    
                    
    morbidmap.close()
    print('finish filling diseases')
    messages.add_message(request, messages.INFO, "Finished filling diseases")
    return redirect('/databases/')

@staff_member_required
def populate_genes(request):
    refgene = open('data/refgene', 'r')
    genes_coords = {}
    for line in refgene:
        if not line.startswith('#'):
            line = line.split('\t')
            gene_name = line[12]
            gene = {}
            gene['chr_location'] = line[2]
            gene['strand'] = line[3]
            #fix for coordinated + 1
            
            gene['txStart'] = int(line[4]) + 1
            gene['txEnd'] = int(line[5]) + 1
            gene['cdsStart'] = int(line[6]) + 1
            gene['cdsEnd'] = int(line[7]) + 1
            gene['exonCount'] = line[8]
            exons_start =  []
            for exon in line[9].split(','):
                if exon != '': 
                    exons_start.append(int(exon) + 1)
            gene['exonStarts'] = ','.join(map(str, exons_start))
            exons_end =  []
            for exon in line[10].split(','):
                if exon != '': 
                    exons_end.append(int(exon) + 1)
                    
            gene['exonEnds'] = ','.join(map(str, exons_end))
            genes_coords[gene_name] = gene
    print('finish loading refseq!!') 
    print(len(genes_coords))
    genes = Gene.objects.all()
    for gene in genes:
#        print gene.official_name
        if gene.official_name in genes_coords:
            gene.chr_location = genes_coords[gene.official_name]['chr_location']
            gene.strand = genes_coords[gene.official_name]['strand']
            gene.transcription_start = genes_coords[gene.official_name]['txStart']
            gene.transcription_end = genes_coords[gene.official_name]['txEnd']
            gene.cds_start = genes_coords[gene.official_name]['cdsStart']
            gene.cds_end = genes_coords[gene.official_name]['cdsEnd']
            gene.exons_count = genes_coords[gene.official_name]['exonCount']
            gene.exons_start = genes_coords[gene.official_name]['exonStarts']
            gene.exons_end = genes_coords[gene.official_name]['exonEnds']
            gene.save()
    print('finish filling genes!!')    
    messages.add_message(request, messages.INFO, "Finished filling genes: %s " % (len(genes_coords)))
    return redirect('/databases/')
 

@login_required
def list(request):
    diseases = Disease.objects.all()
    return render(request, 'diseases/list.html', {'diseases': diseases})
 

@login_required
def view(request, disease_id):
    disease = get_object_or_404(Disease, pk=disease_id)
    gene = disease.gene_set.all()[0]
    # print 'gene', gene.official_name
    # individuals = Individual.objects.all()
    individuals_variants = Variant.objects.filter(gene=gene.official_name)
    # individuals_variants = []
    # for individual in individuals:
    #     individual_variants = Variant.objects.filter(individual=individual, gene=gene.official_name)
    #     individuals_variants.append(individual_variants)
#    individual_variants.query.group_by = ['individual_id']
#    results = query.execute_sql()
#    individuals = Individual.objects.all()
#    for individual in individuals:
#        individual_variants = Variant.objects.find(filter(date__range=["2011-01-01", "2011-01-31"]))
    
    
    return render(request, 'diseases/view.html', {'disease': disease, 'variants': individuals_variants})
    
@staff_member_required
def populate_hgmd_genes(request):
    hgmd_dir = '/projects/hgmd/hgmd'
    listing = os.listdir(hgmd_dir)
    genes_list = []
    for genes_file in listing:
        if genes_file.endswith('html'):
            print(genes_file)
            gfile = '%s/%s' % (hgmd_dir, genes_file)
            soup = BeautifulSoup(open(gfile))
            
            tables = soup.table.findAll('table')
            for row in tables[3]:
                # print row.contents[2].string
                if row.contents[2].string != 'Gene description':
                    # # print row.contents
                    # for item in row.contents:
                    #   print item
                    # print row.contents[0].a.string
                    symbol = row.contents[0].a.string
                    aliases = ''
                    if len(row.contents[0].font.contents) > 1:
                        aliases = row.contents[0].font.contents[1]

                    description = row.contents[2].contents[0]
                    description_aliases = ''
                    if len(row.contents[2].contents[1].font.contents) > 1:
                        description_aliases = row.contents[2].contents[1].font.contents[1]

                    location = row.contents[3].string
                    n_mutations = int(row.contents[5].contents[0].contents[0].contents[0]['value'])


                    gene = HGMDGene(
                        symbol=symbol, 
                        aliases=aliases, 
                        description=description,
                        description_aliases = description_aliases,
                        location=location,
                        n_mutations = n_mutations,
                        )
                    genes_list.append(gene)
    HGMDGene.objects.bulk_create(genes_list)
    messages.add_message(request, messages.INFO, "Finished filling HGMD genes: %s " % (len(genes_list)))
    return redirect('/databases/')
                    




@staff_member_required
def populate_hgmd_mutations(request):
    hgmd_dir = '/projects/hgmd/hgmd/genes/'
    listing = os.listdir(hgmd_dir)
    mutation_list = []
    mutation_counter = 0

    for genes_file in listing:
        if genes_file.endswith('html'):
            # print genes_file
            gfile = '%s/%s' % (hgmd_dir, genes_file)
            # gfile = '%s/C9orf72.html' % (hgmd_dir)
            soup = BeautifulSoup(open(gfile), "html.parser")
            if len(mutation_list) > 5000:
                # print '5000'
                print('mutation_counter', mutation_counter)
                HGMDMutation.objects.bulk_create(mutation_list)
                mutation_list = []

            
            # print soup.contents[1].contents[2].contents[1].contents[1].contents[2].contents[1].a.string
            #soup.prettify()
            # for 
            gene_name = soup.contents[1].contents[2].contents[1].contents[1].contents[2].contents[1].a.string
            # print gene_name
            # gene = gene_name
            gene = HGMDGene.objects.filter(symbol__exact=str(gene_name))[0]
            # print gene

            #loop of each type of mutation
            
            # print 'Hello antes de loop'

            # print soup.contents[1].contents[2].contents[1].contents[1].contents[2].contents
            index = 0
            for row in soup.contents[1].contents[2].contents[1].contents[1].contents[2].contents:
                # print row
                if index >3:
                    if row.name == 'h3':
                        # print 'found mutation type'
                        
                        mutation_type = str(row.contents[0].split(' : ')[0]).strip()
                        
                        # print mutation_type
                        #create a new mutation to insert at the database
                        
                        table_with_mut = soup.contents[1].contents[2].contents[1].contents[1].contents[2].contents[index+1]
                        
                        rows = table_with_mut.find_all("tr")[1:]
                        # print 'number of mutations: %s' % len(rows)
                        
                        for mutation in rows:
                            mutation_counter += 1
                            mutation_record = HGMDMutation()
                            mutation_record.gene = gene
                            mutation_record.mutation_type = mutation_type
                            # print 'mutation'
                            mutation_record.acession = mutation.contents[0].contents[0].contents[0].contents[0].contents[0]['value']
                            if mutation_type == 'Missense/nonsense':
                                # print mutation
                                mutation_record.codon_change = mutation.contents[1].string
                                mutation_record.aa_change = mutation.contents[2].string
                                mutation_record.hgvs_nucleotide = mutation.contents[3].string
                                mutation_record.hgvs_protein = mutation.contents[4].string
                                phenotype = mutation.contents[5].string
                                mutation_record.reference = mutation.contents[6].a
                                extra_information = mutation.contents[7]
                                mutation_record.extras = extra_information.contents[0]

                            elif mutation_type == 'Splicing':
                                
                                mutation_record.splicing_mutation = mutation.contents[1].string
                                mutation_record.hgvs_nucleotide = mutation.contents[2].string

                                phenotype = mutation.contents[3].string
                                mutation_record.reference = mutation.contents[4].a
                                extra_information = mutation.contents[5]
                                mutation_record.extras = extra_information.contents[0]

                            elif mutation_type == 'Regulatory':
                                
                                # regulatory_sequence = " ".join(mutation.contents[1](text=True))
                                mutation_record.regulatory_sequence = " ".join(mutation.contents[1](text=True))
                                phenotype = mutation.contents[2].string
                                mutation_record.reference = mutation.contents[3].a
                                extra_information = mutation.contents[4]
                                mutation_record.extras = extra_information.contents[0]

                            elif mutation_type == 'Small deletions':
                                
                                mutation_record.deletion_sequence = " ".join(mutation.contents[1](text=True))
                                mutation_record.hgvs_nucleotide = mutation.contents[2].string
                                phenotype = mutation.contents[3].string
                                mutation_record.reference = mutation.contents[4].a
                                extra_information = mutation.contents[5]
                                mutation_record.extras = extra_information.contents[0]

                            elif mutation_type == 'Small insertions':
                                
                                mutation_record.insertion_sequence = "".join(mutation.contents[1](text=True))
                                mutation_record.hgvs_nucleotide = mutation.contents[2].string
                                phenotype = mutation.contents[3].string
                                mutation_record.reference = mutation.contents[4].a
                                extra_information = mutation.contents[5]
                                mutation_record.extras = extra_information.contents[0]
                            elif mutation_type == 'Small indels':
                                
                                mutation_record.deletion_sequence = "".join(mutation.contents[1](text=True))
                                mutation_record.insertion_sequence = mutation.contents[2]
                                mutation_record.hgvs_nucleotide = mutation.contents[3].string
                                phenotype = mutation.contents[4].string
                                mutation_record.reference = mutation.contents[5].a
                                extra_information = mutation.contents[6]
                                mutation_record.extras = extra_information.contents[0]

                            elif mutation_type == 'Gross deletions':
                                
                                mutation_record.dna_level = mutation.contents[1].string
                                mutation_record.description = mutation.contents[2].string
                                phenotype = mutation.contents[3].string
                                mutation_record.reference = mutation.contents[4].a
                                extra_information = mutation.contents[5]
                                mutation_record.extras = extra_information.contents[0]

                            elif mutation_type == 'Gross insertions':
                                
                                mutation_record.dna_level = mutation.contents[1].string
                                mutation_record.insertion_duplication = mutation.contents[2].string
                                mutation_record.description = mutation.contents[3].string
                                phenotype = mutation.contents[4].string
                                mutation_record.reference = mutation.contents[5].a
                                extra_information = mutation.contents[6]
                                mutation_record.extras = extra_information.contents[0]
                            elif mutation_type == 'Complex rearrangements':
                                
                                mutation_record.description = mutation.contents[1].string
                                phenotype = mutation.contents[2].string
                                mutation_record.reference = mutation.contents[3].a
                                extra_information = mutation.contents[4]
                                mutation_record.extras = extra_information.contents[0]
                            elif mutation_type == 'Repeat variations':
                                
                                mutation_record.amplified_sequence = mutation.contents[1].string
                                mutation_record.location = mutation.contents[2].string
                                mutation_record.normal_range = mutation.contents[3].string
                                mutation_record.pathological_range = mutation.contents[4].string
                                phenotype = mutation.contents[5].string
                                mutation_record.reference = mutation.contents[6].a
                                extra_information = mutation.contents[7]
                                mutation_record.extras = extra_information.contents[0]



                            else:
                                   print(mutation_type)
                                   die()

                            # print extra_information
                            # print '#loop over extra'
                            # print extra_information
                            for item in extra_information.contents[0]:
                                # print 'item'
                                # print type(item)
                                # print item
                                # if type(item)==bs4.element.NavigableString:
                                    # print 'item'
                                    # print item
                                
                                if type(item)==bs4.element.Tag:
                                    # print 'item'
                                    # print item
                                    # print item['title']
                                    if item.name == 'img':
                                        if item['title'].startswith('Coordinate Chr'):
                                            mutation_record.coordinate = item['title'].split('Coordinate Chr ')[1]
                                            mutation_record.chromossome = mutation_record.coordinate.split(': ')[0]
                                            mutation_record.position = mutation_record.coordinate.split(': ')[1]
                                        # if item['title'] == 'Disease causing mutation':
                                        #     print 'Foudn disease causing mutation!!!'
                                        #     mutation_record.dm_mutation = True

                                    elif item.name == 'a':
                                        # print item.img['alt']
                                        if item.img['alt'].startswith('dbSNP ID'):
                                            mutation_record.rsid = item.img['alt'].split('dbSNP ID: ')[1]
                                            # print rsid
                                        else:
                                            print(item)
                                            print('algo estranho!')
                                            die()
                            #time to insert mutation at the database


                            #save one record and die
                            #get phenotype to save
                            try:
                                pheno = HGMDPhenotype.objects.get(name=phenotype.encode('utf-8'))
                            except HGMDPhenotype.DoesNotExist:
                                #create one
                                pheno = HGMDPhenotype(name=phenotype.encode('utf-8'))
                                pheno.save()
                                gene.diseases.add(pheno)
                                
                            # pheno.genes.add(gene)
                            mutation_record.phenotype = pheno
                            # mutation_record.save()
                            # die()

                            mutation_list.append(mutation_record)
                index += 1

    # print 'mutation_counter', mutation_counter
    # print 'inseringo Bulk!'
    HGMDMutation.objects.bulk_create(mutation_list)
    messages.add_message(request, messages.INFO, "Finished filling HGMD mutations:")
    return redirect('/databases/')

  # hgmd_dir = '/projects/hgmd/hgmd/genes/'
  # listing = os.listdir(hgmd_dir)
  # mutation_list = []
  # count = 0
  # gene_count = 0
  # for genes_file in listing:
  #     if genes_file.endswith('html'):
        
  #       gene_count += 1

  #       if gene_count == 2:
  #           die()

  #       print 'genes_file', genes_file
  #       print 'gene_count', gene_count

  #       gfile = '%s/%s' % (hgmd_dir, genes_file)
  #       # gfile = '%s/C9orf72.html' % (hgmd_dir)
  #       soup = BeautifulSoup(open(gfile), "html.parser")

  #       if len(mutation_list) > 5000:
  #           print '5000'
  #           HGMDMutation.objects.bulk_create(mutation_list)
  #           mutation_list = []
  #       # print soup.contents[1].contents[2].contents[1].contents[1].contents[2].contents[1].a.string
  #       #soup.prettify()
  #       # for 
  #       gene_name = soup.contents[1].contents[2].contents[1].contents[1].contents[2].contents[1].a.string
  #       print 'gene_name', gene_name
  #       # gene = gene_name
  #       gene = HGMDGene.objects.filter(symbol__exact=str(gene_name))[0]
  #       # print gene

  #       #loop of each type of mutation
        
  #       print 'Hello antes de loop'
  #       #create a pattern to get mutattions
  #       print soup#.contents[1].contents[2].contents[1].contents[1].contents[2]#.contents
  #       die()
  #       index = 0
  #       for row in soup.contents[1].contents[2].contents[1].contents[1].contents[2].contents:
          
          
  #         if index > 3:
  #           if row.name == 'h3':
  #             print 'found mutation type'
              
  #             mutation_type = str(row.contents[0].split(' : ')[0]).strip()
              
  #             print mutation_type
  #             #create a new mutation to insert at the database
              
  #             table_with_mut = soup.contents[1].contents[2].contents[1].contents[1].contents[2]#.contents[index+1]
  #             print 'table mut', table_with_mut
  #             die()

  #             rows = table_with_mut.find_all("tr")[1:]
  #             print 'number of mutations: %s' % len(rows)
              
  #             for mutation in rows:
  #               mutation_record = HGMDMutation()
  #               mutation_record.gene = gene
  #               mutation_record.mutation_type = mutation_type
  #               # print 'mutation'
  #               mutation_record.acession = mutation.contents[0].contents[0].contents[0].contents[0].contents[0]['value']
  #               if mutation_type == 'Missense/nonsense':
  #                 # print mutation
  #                 mutation_record.codon_change = mutation.contents[1].string
  #                 mutation_record.aa_change = mutation.contents[2].string
  #                 mutation_record.hgvs_nucleotide = mutation.contents[3].string
  #                 mutation_record.hgvs_protein = mutation.contents[4].string
  #                 phenotype = mutation.contents[5].string
  #                 mutation_record.reference = mutation.contents[6].a
  #                 extra_information = mutation.contents[7]
  #                 mutation_record.extras = extra_information.contents[0]

  #               elif mutation_type == 'Splicing':
                  
  #                 mutation_record.splicing_mutation = mutation.contents[1].string
  #                 mutation_record.hgvs_nucleotide = mutation.contents[2].string

  #                 phenotype = mutation.contents[3].string
  #                 mutation_record.reference = mutation.contents[4].a
  #                 extra_information = mutation.contents[5]
  #                 mutation_record.extras = extra_information.contents[0]

  #               elif mutation_type == 'Regulatory':
                  
  #                 # regulatory_sequence = " ".join(mutation.contents[1](text=True))
  #                 mutation_record.regulatory_sequence = " ".join(mutation.contents[1](text=True))
  #                 phenotype = mutation.contents[2].string
  #                 mutation_record.reference = mutation.contents[3].a
  #                 extra_information = mutation.contents[4]
  #                 mutation_record.extras = extra_information.contents[0]

  #               elif mutation_type == 'Small deletions':
                  
  #                 mutation_record.deletion_sequence = " ".join(mutation.contents[1](text=True))
  #                 mutation_record.hgvs_nucleotide = mutation.contents[2].string
  #                 phenotype = mutation.contents[3].string
  #                 mutation_record.reference = mutation.contents[4].a
  #                 extra_information = mutation.contents[5]
  #                 mutation_record.extras = extra_information.contents[0]

  #               elif mutation_type == 'Small insertions':
                  
  #                 mutation_record.insertion_sequence = "".join(mutation.contents[1](text=True))
  #                 mutation_record.hgvs_nucleotide = mutation.contents[2].string
  #                 phenotype = mutation.contents[3].string
  #                 mutation_record.reference = mutation.contents[4].a
  #                 extra_information = mutation.contents[5]
  #                 mutation_record.extras = extra_information.contents[0]
  #               elif mutation_type == 'Small indels':
                  
  #                 mutation_record.deletion_sequence = "".join(mutation.contents[1](text=True))
  #                 mutation_record.insertion_sequence = mutation.contents[2]
  #                 mutation_record.hgvs_nucleotide = mutation.contents[3].string
  #                 phenotype = mutation.contents[4].string
  #                 mutation_record.reference = mutation.contents[5].a
  #                 extra_information = mutation.contents[6]
  #                 mutation_record.extras = extra_information.contents[0]

  #               elif mutation_type == 'Gross deletions':
                  
  #                 mutation_record.dna_level = mutation.contents[1].string
  #                 mutation_record.description = mutation.contents[2].string
  #                 phenotype = mutation.contents[3].string
  #                 mutation_record.reference = mutation.contents[4].a
  #                 extra_information = mutation.contents[5]
  #                 mutation_record.extras = extra_information.contents[0]

  #               elif mutation_type == 'Gross insertions':
                  
  #                 mutation_record.dna_level = mutation.contents[1].string
  #                 mutation_record.insertion_duplication = mutation.contents[2].string
  #                 mutation_record.description = mutation.contents[3].string
  #                 phenotype = mutation.contents[4].string
  #                 mutation_record.reference = mutation.contents[5].a
  #                 extra_information = mutation.contents[6]
  #                 mutation_record.extras = extra_information.contents[0]
  #               elif mutation_type == 'Complex rearrangements':
                  
  #                 mutation_record.description = mutation.contents[1].string
  #                 phenotype = mutation.contents[2].string
  #                 mutation_record.reference = mutation.contents[3].a
  #                 extra_information = mutation.contents[4]
  #                 mutation_record.extras = extra_information.contents[0]
  #               elif mutation_type == 'Repeat variations':
                  
  #                 mutation_record.amplified_sequence = mutation.contents[1].string
  #                 mutation_record.location = mutation.contents[2].string
  #                 mutation_record.normal_range = mutation.contents[3].string
  #                 mutation_record.pathological_range = mutation.contents[4].string
  #                 phenotype = mutation.contents[5].string
  #                 mutation_record.reference = mutation.contents[6].a
  #                 extra_information = mutation.contents[7]
  #                 mutation_record.extras = extra_information.contents[0]

  #               else:
  #                  print mutation_type
  #                  die()

  #               # print extra_information
  #               # print '#loop over extra'
  #               # print extra_information
  #               extra_information = extra_information.find_all()
  #               # print extra_information

  #               for item in extra_information:#.contents[0]
  #                 # print 'item'
  #                 # print type(item)
  #                 # print item
  #                 # if type(item)==bs4.element.NavigableString:
  #                   # print 'item'
  #                   # print item
                  
  #                 if type(item)==bs4.element.Tag:
  #                   # print 'item'
  #                   # print item
  #                   # print item['title']
  #                   if item.name == 'img':
  #                     # print 'img'
  #                     # print item['title'] 
  #                     if item['title'].startswith('Coordinate Chr'):
  #                       mutation_record.coordinate = item['title'].split('Coordinate Chr ')[1]
  #                       mutation_record.chromossome = mutation_record.coordinate.split(': ')[0]
  #                       mutation_record.position = mutation_record.coordinate.split(': ')[1]
  #                     if item['title'] == 'Disease causing mutation':
  #                        # print 'Foudn disease causing mutation!!!'
  #                        mutation_record.dm_mutation = True

  #                   elif item.name == 'a':
  #                     # print item.img['alt']
  #                     if item.img['alt'].startswith('dbSNP ID'):
  #                       mutation_record.rsid = item.img['alt'].split('dbSNP ID: ')[1]
  #                       # print rsid
  #                   else:
  #                     print item
  #                     print 'algo estranho!'
  #                     die()
  #               #time to insert mutation at the database
  #               #save one record and die
  #               #get phenotype to save
  #               try:
  #                 pheno = HGMDPhenotype.objects.get(name=phenotype.encode('utf-8').strip())
  #               except HGMDPhenotype.DoesNotExist:
  #                 #create one
  #                 pheno = HGMDPhenotype(name=phenotype.encode('utf-8').strip())
  #                 pheno.save()
  #                 gene.diseases.add(pheno)

                  
  #               # pheno.genes.add(gene)
  #               mutation_record.phenotype = pheno
  #               # mutation_record.save()
  #               # die()
  #               count += 1
  #               print count
  #               mutation_list.append(mutation_record)
  #         index += 1
  #       #end of first gene
