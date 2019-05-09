from django.core.management.base import BaseCommand, CommandError
# from polls.models import Poll
from genes.models import *
import codecs

from diseases.models import *

from genes.models import Gene as Gene2

import os
import zipfile

def populate_genes():
    #populate genes from hgnc
    Gene2.objects.all().delete()

    # zip_file    = zipfile.ZipFile(sys.argv[1])
    zip = zipfile.ZipFile('data/hgnc/hgnc_complete_set.txt.zip', 'r')
    hgnc = zip.open('hgnc_complete_set.txt', 'r')
    # hgnc = codecs.open('data/hgnc/hgnc_complete_set.txt', 'r', "ISO-8859-1")
    header = hgnc.readline().decode("utf-8").strip().split('\t')
    count_gene = 1
    
    genes = []
    countline = 0
    for lineb in hgnc:
#        print count_gene
        line = lineb.decode("utf-8")

        count_gene += 1
        countline += 1
        #print countline
        if count_gene == 5000:
            print(countline)
            #bulk_insert(genes, show_sql=False)
            Gene2.objects.bulk_create(genes)
            count_gene = 0
            genes = []
        
#        print line
        line = line.strip().split('\t')
        # print(len(line))
        # print(line)
        #ugly hack, to fill missing fields ?
        if len(line) != 48:
            count = 48 - len(line) 
            for item in range(0,count):
                line.append('')
        
        gene = Gene2(
                    hgnc_id = line[0],
                    symbol = line[1],
                    name = line[2],
                    locus_group = line[3],
                    locus_type = line[4],
                    status = line[5],
                    location = line[6],
                    location_sortable = line[7],
                    alias_symbol = line[8],
                    alias_name = line[9],
                    prev_symbol = line[10],
                    prev_name = line[11],
                    gene_family = line[12],
                    gene_family_id = line[13],
                    date_approved_reserved = line[14],
                    date_symbol_changed = line[15],
                    date_name_changed = line[16],
                    date_modified = line[17],
                    entrez_id = line[18],
                    ensembl_gene_id = line[19],
                    vega_id = line[20],
                    ucsc_id = line[21],
                    ena = line[22],
                    refseq_accession = line[23],
                    ccds_id = line[24],
                    uniprot_ids = line[25],
                    pubmed_id = line[26],
                    mgd_id = line[27],
                    rgd_id = line[28],
                    lsdb = line[29],
                    cosmic = line[30],
                    omim_id = line[31],
                    mirbase = line[32],
                    homeodb = line[33],
                    snornabase = line[34],
                    bioparadigms_slc = line[35],
                    orphanet = line[36],
                    pseudogene_org = line[37],
                    horde_id = line[38],
                    merops = line[39],
                    imgt = line[40],
                    iuphar = line[41],
                    kznf_gene_catalog = line[42],
                    mamit_trnadb = line[43],
                    cd = line[44],
                    lncrnadb = line[45],
                    enzyme_id = line[46],
                    intermediate_filament_db = line[47]
                )
    
        
        genes.append(gene)

    Gene2.objects.bulk_create(genes)
    #bulk_insert(genes, show_sql=False)
    hgnc.close()

def populate_diseases():
    # print os.getcwd()

    Gene.objects.all().delete()
    Disease.objects.all().delete()
   
    if os.path.isfile('data/omim/morbidmap.txt'):

        morbidmap = open('data/omim/morbidmap.txt', 'r')
        for line in morbidmap:
            # print(line)
            if not line.startswith('#'):
                line = line.split('\t')
                name = line[0]
                omim_id = line[2]
                chr_location = line[3].strip()
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
                        pass
                        
        morbidmap.close()

def populate_CGD():

    CGDCondition.objects.all().delete()
    Manifestation.objects.all().delete()
    Intervention.objects.all().delete()
    CGDEntry.objects.all().delete()


    zip = zipfile.ZipFile('data/CGD/CGD.txt.zip', 'r')
    CDGfile = zip.open('CGD.txt', 'r')

    # CDGfile = open('data/CGD/CGD.txt')
    header = next(CDGfile)
    for lineb in CDGfile:
        line = lineb.decode('utf-8')
        gene_item = line.split('\t')
        # print gene_item
        cgd = CGDEntry()

        cgd.GENE = gene_item[0]
        cgd.HGNC_ID = gene_item[1]
        cgd.ENTREZ_GENE_ID = gene_item[2]
        
        cgd.INHERITANCE = gene_item[4]
        cgd.AGE_GROUP = gene_item[5]
        cgd.ALLELIC_CONDITIONS = gene_item[6]

        cgd.COMMENTS = gene_item[9]
        cgd.INTERVENTION_RATIONALE = gene_item[10]
        
        references_list =[]
        references = gene_item[11].split(';')
        for ref in references:
            references_list.append(ref.strip())

        cgd.REFERENCES = references_list

        cgd.save()

        conditions = gene_item[3].split(';')
        for condition in conditions:
            condition = condition.strip()
            if condition != '':
                cond_obj = CGDCondition.objects.get_or_create(name=condition)[0]
                cgd.CONDITIONS.add(cond_obj)
                # cgd.CONDITIONS.append(cond_obj)

        manifestations = gene_item[7].split(';')
        for manifestation in  manifestations:
            #try get manifestation
            manifestation = manifestation.strip()
            if manifestation != '':
                man_obj = Manifestation.objects.get_or_create(name=manifestation)[0]
                cgd.MANIFESTATION_CATEGORIES.add(man_obj)
                # cgd.MANIFESTATION_CATEGORIES.append(man_obj)  
                

        interventions = gene_item[8].split(';')
        for intervention in  interventions:
            #try get manifestation
            intervention = intervention.strip()
            int_obj = Intervention.objects.get_or_create(name=intervention)[0]
            cgd.INTERVENTION_CATEGORIES.add(int_obj)
            # cgd.INTERVENTION_CATEGORIES.append(int_obj)

        
class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Populate data from diseases and genes'

    def handle(self, *args, **options):

        print('Populate Genes!')
        populate_genes()
        print('Populate Diseases from OMIM!')
        populate_diseases()
        #populate diseases from OMIM
        print('Populate Diseases from CGD!')
        populate_CGD()
        #populate dieases from CGD
        #populate dieases from CGD


        # for poll_id in args:
        #     try:
        #         poll = Poll.objects.get(pk=int(poll_id))
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write('Successfully closed poll "%s"' % poll_id)
