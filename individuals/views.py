import gzip
import json
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
from django.utils.text import slugify
from django.views.generic import DeleteView
from individuals.forms import IndividualForm, ComparisonForm, GroupForm, BrowserForm
from individuals.models import Individual, Group
from individuals.tasks import VerifyVCF, AnnotateVariants, PopulateVariants
from variants.models import Variant

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = json.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

def create(request):
    if request.method == 'POST':
        form = IndividualForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            if request.user.is_authenticated:
                individual = Individual.objects.create(user=request.user, status='new')
            else:
                individual = Individual.objects.create(user=None, status='new')

            individual.vcf_file= request.FILES.get('file')
            
            print('file')
            print(request.FILES.get('file'))

            filename = individual.vcf_file.name.split('.')
            new_filename = [] 
            for tag in filename:
                new_filename.append(slugify(tag))

            individual.vcf_file.name = ".".join(new_filename)

            # print('filename ', filename)

            #get name from inside vcf file
            individual.name= str(os.path.splitext(individual.vcf_file.name)[0]).replace('.vcf','').replace('.gz','').replace('.rar','').replace('.zip','').replace('._',' ').replace('.',' ')

            # individual.shared_with_groups = form.cleaned_data['shared_with_groups']

            individual.shared_with_groups.set(form.cleaned_data['shared_with_groups'])
            
            individual.save()
            
            f = individual.vcf_file
            
            #fix permissions
            #os.chmod("%s/genomes/%s/" % (settings.BASE_DIR, individual.user), 0777)

            if request.user.is_authenticated:

                os.chmod("%s/genomes/%s/%s" % (settings.BASE_DIR, slugify(individual.user), individual.id), 0o777)
            else:
                os.chmod("%s/genomes/public/%s" % (settings.BASE_DIR, individual.id), 0o777)

            # AnnotateVariants.delay(individual.id)
            VerifyVCF.delay(individual.id)

            data = {'files': [{'deleteType': 'DELETE', 'name': individual.name, 'url': '', 'thumbnailUrl': '', 'type': 'image/png', 'deleteUrl': '', 'size': f.size}]}

            response = JSONResponse(data, mimetype=response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'

            return response
        else:
            print(form.errors)

    else:
        form = IndividualForm()

    return render(request, 'individuals/create.html', {'form':form})

# Create your views here.
@login_required
def edit(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    if request.method == 'POST':
        form = IndividualForm(request.POST, instance=individual)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    #     form = IndividualForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         individual = form.save(commit=False)
    #         individual.user = request.user
    #         individual.save()
    #         return redirect('dashboard')
    else:
        form = IndividualForm(instance=individual)

    return render(request, 'individuals/individual_form.html', {'form':form})


class IndividualDeleteView(DeleteView):
    model = Individual

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        individual_id = self.object.id

        if self.object.user:
            username = self.object.user.username
        else:
            username = 'public'
        
        #delete files
        if self.object.vcf_file:
            self.object.vcf_file.delete()

        # if self.object.strs_file:
        #     self.object.strs_file.delete()
        # if self.object.cnvs_file:
        #     self.object.cnvs_file.delete()
        os.system('rm -rf %s/genomes/%s/%s' % (settings.BASE_DIR, username, individual_id))

        self.object.delete()
        
        
        
        
#        response = JSONResponse(True, {}, response_mimetype(self.request))
#        response['Content-Disposition'] = 'inline; filename=files.json'
#        return response
        messages.add_message(request, messages.INFO, "Individual deleted with success!")
        #return redirect('individuals_list')
        return redirect('individuals_list')


def view(request, individual_id):

    individual = get_object_or_404(Individual, pk=individual_id)

    variant_list = Variant.objects.filter(individual=individual)
    # snpeff = SnpeffAnnotation.objects.filter(individual=individual)

    individual.n_variants = variant_list.count()
    individual.novel_variants = variant_list.filter(variant_id = '.').count()

    individual.summary = []

    #get calculated values from database

    summary_item = {
                'type': 'Total SNVs',
                'total': variant_list.values('genotype').count(),
                'discrete': variant_list.values('genotype').annotate(total=Count('genotype'))
                    }
    individual.summary.append(summary_item)

    summary_item = {
                'type': 'Total Gene-associated SNVs',
                'total': variant_list.values('gene').exclude(gene="").count(),
                'discrete': variant_list.exclude(gene="").values('genotype').annotate(total=Count('genotype'))
                    }
    individual.summary.append(summary_item)

    individual.snp_eff = variant_list.values('snpeff_effect').annotate(Count('snpeff_effect')).order_by('snpeff_effect')
    # print 'individual.snp_eff', individual.snp_eff
    # variant_list.values('snpeff__effect').annotate(Count('snpeff__effect')).order_by('snpeff__effect')
    #
    individual.functional_class = variant_list.values('snpeff_func_class').annotate(Count('snpeff_func_class')).order_by('snpeff_func_class')
    individual.impact_variants = variant_list.values('snpeff_impact').annotate(Count('snpeff_impact')).order_by('snpeff_impact')

    individual.filter_variants = variant_list.values('filter').annotate(Count('filter')).order_by('filter')
    individual.quality = variant_list.aggregate(Avg('qual'), Max('qual'), Min('qual'))
    individual.read_depth = variant_list.aggregate(Avg('read_depth'), Max('read_depth'), Min('read_depth'))

    individual.clinvar_clnsig = variant_list.values('clinvar_clnsig').annotate(total=Count('clinvar_clnsig'))

    individual.chromossome = variant_list.values('chr').annotate(total=Count('chr')).order_by('chr')

    # variants_with_snpid = variant_list.values('variant_id').exclude(variant_id=".")
    #print variants_with_snpid

    # fields = Variant._meta.get_all_field_names()

    paginator = Paginator(variant_list, 25) # Show 25 contacts per page
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
    #'fields':fields
    return render(request, 'individuals/view.html', {'individual': individual, 'variants':variants})

@login_required
def browse(request, individual_id):

    query_string = request.META['QUERY_STRING']
    individual = get_object_or_404(Individual, pk=individual_id)
    query = {}
    
#    DEFAULT_SORT = 'pk'
#    sort_key = request.GET.get('sort', DEFAULT_SORT)
    # tags = ['genotype', 'snpeffannotation__effect']#, 'func_class', 'impact', 'cln_omim', 'chr' 
    # for tag in tags:
    #     criteria = request.GET.get(tag, '')
    #     if criteria:
    #         query[tag] = criteria

    
    if request.method == 'GET':
        form = BrowserForm(request.GET)   
        if form.is_valid():
            print('form is valid')
            #chr
            chr = request.GET.get('chr', '')
            if chr != '':
                query['chr'] = chr
            #pos
            pos = request.GET.get('pos', '')
            if pos != '':
                query['pos'] = pos

            effect = request.GET.get('effect', '')
            if effect != '':
                print('effect', effect)
                query['snpeff_effect'] = effect                
            #snp_id
            # snp_id = request.GET.get('snp_id', '')
            # if snp_id != '':
            #     query['variant_id'] = snp_id
            # snp_list = request.GET.get('snp_list', '')
            # snp_list = snp_list.split('\r\n')
            # if snp_list[0] != u'':
            #     query['variant_id__in'] = snp_list
            # snp_eff = request.GET.getlist('effect')
            # if len(snp_eff) > 0:
            #     query['snp_eff__in'] = snp_eff
            # func_class = request.GET.getlist('func_class')
            # if len(func_class) > 0:
            #     query['snp_eff_functional_class__in'] = func_class
            # gene = request.GET.get('gene', '')
            # if gene != '':
            #     query['gene_name'] = gene
            # gene_list = request.GET.get('gene_list', '')
            # gene_list = gene_list.split('\r\n')
            # if gene_list[0] != u'':
            #     query['gene_name__in'] = gene_list
            # cln = request.GET.get('cln_omim', '')
            # print 'clnomim', cln
            # if cln == 'on':
            #     query['cln_omim'] != ''

            variants = Variant.objects.filter(individual=individual, **query)

            # snpeff_annotations = SnpeffAnnotation.objects.filter(variant__in=variants)
            # #b.entry_set.filter(headline__contains='Lennon')

            # print 'snpeff_annotations', len(snpeff_annotations)

            # for variant in variants:
            #     print variant.entry_set.all()
            
            #     variant.snpeff=

    
    else:
        
        form = BrowserForm(request.GET)
        variants = Variant.objects.filter(individual=individual, **query)
        
        
    #Pagination
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
    
    return render(request, 'variants/variants.html', {'individual': individual, 'variants':variants, 'form':form, 'query_string':query_string})

@login_required
def list(request):

    if request.method == 'POST':
        individuals = request.POST.getlist('individuals')
        print(individuals) 
        individuals = [int(x) for x in individuals]
        print(individuals)
        
        if request.POST['selectionField'] == "Show":
            for individual_id in individuals:
                individual = get_object_or_404(Individual, pk=individual_id)
                individual.is_featured = True
                individual.save()
        if request.POST['selectionField'] == "Hide":
            for individual_id in individuals:
                individual = get_object_or_404(Individual, pk=individual_id)
                individual.is_featured = False
                individual.save()
        if request.POST['selectionField'] == "Delete":
            for individual_id in individuals:
                individual = get_object_or_404(Individual, pk=individual_id)


                individual_id = individual.id
                username = individual.user.username

                #delete files
                if individual.vcf_file:
                    individual.vcf_file.delete()
                # if individual.strs_file:
                #     individual.strs_file.delete()
                # if individual.cnvs_file:
                #     individual.cnvs_file.delete()
                os.system('rm -rf %s/genomes/%s/%s' % (settings.BASE_DIR, username, individual_id))

                individual.delete()
            #os.system('rm -rf mendelmd14/site_media/media/genomes/%s/%s' % (username, individual_id))
        if request.POST['selectionField'] == "Populate":
            for individual_id in individuals:
                individual = get_object_or_404(Individual, pk=individual_id)
                PopulateVariants.delay(individual.id)
            
        if request.POST['selectionField'] == "Annotate":
            for individual_id in individuals:
                individual = get_object_or_404(Individual, pk=individual_id)
                AnnotateVariants.delay(individual.id)
        if request.POST['selectionField'] == "Find_Medical_Conditions_and_Medicines":
            for individual_id in individuals:
                individual = get_object_or_404(Individual, pk=individual_id)
                Find_Medical_Conditions_and_Medicines.delay(individual.id)
        
    
    args = []
    # groups = Groups.objects.filter(user=request.user, shared_with_users=).order_by("-id")
    args.append(Q(user=request.user) | Q(shared_with_users=request.user) | Q(shared_with_groups__members=request.user))
    
    if request.user.is_staff:
        individuals = Individual.objects.all()
    else:
        individuals = Individual.objects.filter(*args).order_by("-id")
    
    ind_featured = Individual.objects.filter(is_featured= True).order_by("id")
    # paginator = Paginator(individuals, 25) # Show 25 contacts per page
           
    # try:
    #    page = int(request.GET.get('page', '1'))
    # except ValueError:
    #    page = 1
    # try:
    #    individuals = paginator.page(page)
    # except PageNotAnInteger:
    #    # If page is not an integer, deliver first page.
    #    individuals = paginator.page(1)
    # except EmptyPage:
    #    # If page is out of range (e.g. 9999), deliver last page of results.
    #    individuals = paginator.page(paginator.num_pages)



    groups = Group.objects.all()
#    individuals = Individual.objects.annotate(number_of_variants=Count('variant'))
    
    
    return render(request, 'individuals/list.html', {'individuals': individuals, 'groups':groups, 'ind_featured':ind_featured})


@login_required
def annotate(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    individual.status = 'new'
    individual.n_lines = 0
    VerifyVCF.delay(individual.id)
    individual.save()
    messages.add_message(request, messages.INFO, "Your individual is being annotated.")
    return redirect('dashboard')

@login_required
def populate(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    PopulateVariants.delay(individual.id)
    messages.add_message(request, messages.INFO, "Your individual is being populated.")

    return redirect('dashboard')


@login_required
def populate_mongo(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    PopulateMongoVariants.delay(individual.id)
    messages.add_message(request, messages.INFO, "Your individual is being inserted at MongoDB.")

    return redirect('individuals_list')


def download(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    
    filepath = os.path.dirname(str(individual.vcf_file.name))
    filename = os.path.basename(str(individual.vcf_file.name))
    
    path = ''
    # os.chmod("%s/genomes/%s/%s" % (settings.MEDIA_ROOT, individual.user, individual.id), 0777)

    
    # if filename.endswith('vcf.zip'):
       # basename = filename.split('.vcf.zip')[0]       
    # elif filename.endswith('.zip'):
       # basename = filename.split('.zip')[0]       
    # else:
       # basename = filename.split('.vcf')[0]
    #print basename
    #print path
    #print filepath
    
    fullpath = '%s/%s' % (filepath, filename)
    if filename.endswith('.gz'):
        vcffile = gzip.open(fullpath, 'r')
    else:
        vcffile = open(fullpath, 'r')

    content = vcffile.read()
    vcffile.close()

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = os.path.getsize(fullpath)
    return response



def download_annotated(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    
    filepath = os.path.dirname(str(individual.vcf_file.name))
    filename = os.path.basename(str(individual.vcf_file.name))
    
    # path = settings.MEDIA_ROOT
    # if filename.endswith('vcf.zip'):
       # basename = filename.split('.vcf.zip')[0]       
    # else:
    
    basename = filename.split('.vcf')[0]
    
    fullpath = '%s/annotation.final.vcf.zip' % (filepath)

    vcffile = open(fullpath, 'rb')

    response = HttpResponse(vcffile, content_type='application/x-zip-compressed')
    # # response['Content-Encoding'] = 'gzip'
    response['Content-Disposition'] = 'attachment; filename=%s.annotated.mendelmd.vcf.zip' % basename
    response['Content-Length'] = os.path.getsize(fullpath)
    return response

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)        
        if form.is_valid():
            form.save()
            
            return redirect('individuals_list')
    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def view_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    return render(request, 'groups/view_group.html', {'group': group})

class GroupDeleteView(DeleteView):
    model = Group

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        
        #username = self.object.user.username
        
        self.object.delete()
        messages.add_message(request, messages.INFO, "Group deleted with success!")
        return redirect('individuals_list')


def comparison(request):
    query = {}
    summary = {}
    variants = []
    query_string = request.META['QUERY_STRING']
    if request.method == 'GET':
        form = ComparisonForm(request.user, request.GET, request.FILES)        
        if form.is_valid():
            
            individual_one_id = request.GET.get('individual_one', '')
            individual_two_id = request.GET.get('individual_two', '')
            read_depth = request.GET.get('read_depth', '')
            if read_depth != '':
                query['read_depth__gte'] = float(read_depth)
            if individual_one_id != '' and individual_two_id != '': 
                variants_ind_one = Variant.objects.filter(individual__id=individual_one_id, **query).values('chr', 'pos', 'genotype')
                
                variants_ind_two = Variant.objects.filter(individual__id=individual_two_id, **query).values('chr', 'pos', 'genotype')
                print('Got Variants from Both!')
    
                genotypes_in_common = 0
                genotypes_not_in_common = 0
                ind_one = {}
                ind_two = {}
                summary['variants_ind_one'] = variants_ind_one.count()
                 
                for variant in variants_ind_one:
                    id = '%s-%s' % (variant['chr'], variant['pos'])
                    if id in ind_one:                 
                        ind_one[id].append(variant['genotype'])
                    else:
                        ind_one[id] = []
                        ind_one[id].append(variant['genotype'])
                        
                summary['variants_ind_two'] = variants_ind_two.count()
                for variant in variants_ind_two:
                    id = '%s-%s' % (variant['chr'], variant['pos'])
                    if id in ind_two:                 
                        ind_two[id].append(variant['genotype'])
                    else:
                        ind_two[id] = []
                        ind_two[id].append(variant['genotype'])
                    
                
                print('Finished creating indexes')
                for pos in ind_one:
                    if pos in ind_two:
                        for genotype in ind_one[pos]:
                            
                            if genotype in ind_two[pos]:
                                genotypes_in_common += 1
    #                            variant ={}
    #                            variant['chr'] = item.split('-')[0]
    #                            variant['pos'] = item.split('-')[1]
    #                            variant['genotype'] = ind_two[item]
                                
    #                            variants.append(variant) 
                            else:
                                genotypes_not_in_common += 1
                        
    #                        
                print('genotypes in common: %s' % genotypes_in_common)
                summary['genotypes_in_common'] = genotypes_in_common
                summary['genotypes_not_in_common'] = genotypes_not_in_common
                summary['total_variants'] = genotypes_in_common + genotypes_not_in_common
                
                summary['percent_ind_one'] = round((float(genotypes_in_common)/summary['variants_ind_one'])*100, 2)
                summary['percent_ind_two'] = round((float(genotypes_in_common)/summary['variants_ind_two'])*100, 2)
                print(summary)
            
    else:
        form = ComparisonForm(request.user)
        
        
    return render(request, 'individuals/comparison.html', {'form':form, 'summary':summary, 'query_string':query_string})
