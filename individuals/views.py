from django.http import Http404
import gzip
import json
import os
import shutil

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
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse as DjangoJsonResponse
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
from mendelmd.access import owned_groups, owned_variants


def get_owned_individual(request, individual_id):
    """Return the individual only if the requesting user owns it (staff may see all)."""
    individual = get_object_or_404(Individual, pk=individual_id)
    if not request.user.is_staff and individual.user_id != request.user.id:
        raise Http404
    return individual


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
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return JSONResponse({'error': 'No file provided'}, mimetype=response_mimetype(request))

            if request.user.is_authenticated:
                individual = Individual.objects.create(user=request.user, status='new')
            else:
                individual = Individual.objects.create(user=None, status='new')

            # Slugify each dot-separated part of the filename
            parts = uploaded_file.name.split('.')
            uploaded_file.name = ".".join(slugify(tag) for tag in parts)

            individual.vcf_file = uploaded_file

            # Derive a human-readable name from the base filename only
            basename = os.path.basename(uploaded_file.name)
            stem = os.path.splitext(basename)[0]
            individual.name = (
                stem
                .replace('.vcf', '').replace('.gz', '').replace('.rar', '').replace('.zip', '')
                .replace('._', ' ').replace('.', ' ')
                .strip()
            ) or f"Individual {individual.id}"


            individual.save()

            f = individual.vcf_file
            
            #fix permissions
            #os.chmod("%s/genomes/%s/" % (settings.BASE_DIR, individual.user), 0777)

            #if request.user.is_authenticated:

            #    os.chmod("%s/genomes/%s/%s" % (settings.BASE_DIR, slugify(individual.user), individual.id), 0o777)
            #else:
            #    os.chmod("%s/genomes/public/%s" % (settings.BASE_DIR, individual.id), 0o777)

            # AnnotateVariants.delay(individual.id)
            try:
                VerifyVCF.delay(individual.id)
            except Exception as e:
                print('Error dispatching VerifyVCF task:', e)

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
    individual = get_owned_individual(request, individual_id)
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
        shutil.rmtree(os.path.join(settings.BASE_DIR, 'genomes', username, str(individual_id)), ignore_errors=True)

        self.object.delete()
        
        
        
        
#        response = JSONResponse(True, {}, response_mimetype(self.request))
#        response['Content-Disposition'] = 'inline; filename=files.json'
#        return response
        messages.add_message(request, messages.INFO, "Individual deleted with success!")
        #return redirect('individuals_list')
        return redirect('individuals_list')


class _ParquetRows:
    """Sequence over a parquet file that only materialises the slices asked for.

    The sample page shows 50 rows at a time; reading every row into Python
    dicts on each request used several GB for large samples.
    """

    def __init__(self, parquet_file, columns):
        self._pf = parquet_file
        self.columns = columns
        self._n = parquet_file.metadata.num_rows

    def __len__(self):
        return self._n

    def count(self):
        return self._n

    def __getitem__(self, item):
        if not isinstance(item, slice):
            return self[item:item + 1][0]
        start, stop, _ = item.indices(self._n)
        rows, pos = [], 0
        if start >= stop:
            return rows
        for batch in self._pf.iter_batches(batch_size=5000, columns=self.columns):
            end = pos + batch.num_rows
            if end > start:
                lo, hi = max(start - pos, 0), min(stop - pos, batch.num_rows)
                rows.extend(batch.slice(lo, hi - lo).to_pandas().fillna('').to_dict('records'))
            if end >= stop:
                break
            pos = end
        return rows


def _parquet_path(individual):
    username = slugify(individual.user.username) if individual.user else 'public'
    return os.path.join(settings.BASE_DIR, 'genomes', username, str(individual.id),
                        'ann_sample', 'annotation.final.parquet')


def _load_parquet_variants(individual):
    """Return (columns, lazy rows, summary dataframe) for the sample page."""
    try:
        import pyarrow.parquet as pq
        path = _parquet_path(individual)
        if not os.path.exists(path):
            return [], [], None
        pf = pq.ParquetFile(path)
        names = pf.schema_arrow.names
        core = [c for c in ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'VARTYPE'] if c in names]
        vep = [c for c in ['SYMBOL', 'Gene', 'Consequence', 'IMPACT', 'SIFT', 'PolyPhen', 'HGVSc', 'HGVSp', 'BIOTYPE', 'EXON', 'INTRON', 'Amino_acids'] if c in names]
        extra = [c for c in names if c not in core and c not in vep and c not in ('HET', 'HOM')]
        summary_cols = [c for c in ['CHROM', 'VARTYPE', 'FILTER', 'ID'] if c in names]
        summary = pf.read(columns=summary_cols).to_pandas() if summary_cols else None
        return core + vep + extra, _ParquetRows(pf, core + vep + extra), summary
    except Exception:
        return [], [], None


def _counts(summary, column):
    if summary is None or column not in summary:
        return []
    values = summary[column].dropna().astype(str)
    values = values[values != '']
    return sorted(values.value_counts().items())


def view(request, individual_id):

    individual = get_owned_individual(request, individual_id)

    parquet_columns, parquet_rows, summary = _load_parquet_variants(individual)

    individual.n_variants = len(parquet_rows)
    if summary is not None and 'ID' in summary:
        ids = summary['ID'].fillna('').astype(str)
        individual.novel_variants = int(ids.isin(['', '.']).sum())
    else:
        individual.novel_variants = 0

    individual.chromossome = [{'chr': k, 'total': int(v)} for k, v in _counts(summary, 'CHROM')]
    individual.vartype_summary = [{'vartype': k, 'total': int(v)} for k, v in _counts(summary, 'VARTYPE')]
    individual.filter_variants = [{'filter': k, 'filter__count': int(v)} for k, v in _counts(summary, 'FILTER')]

    paginator = Paginator(parquet_rows, 50)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        variants = paginator.page(page)
    except PageNotAnInteger:
        variants = paginator.page(1)
    except EmptyPage:
        variants = paginator.page(paginator.num_pages)

    return render(request, 'individuals/view.html', {
        'individual': individual,
        'variants': variants,
        'parquet_columns': parquet_columns,
    })

@login_required
def browse(request, individual_id):

    query_string = request.META['QUERY_STRING']
    individual = get_owned_individual(request, individual_id)
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
                individual = get_owned_individual(request, individual_id)
                individual.is_featured = True
                individual.save()
        if request.POST['selectionField'] == "Hide":
            for individual_id in individuals:
                individual = get_owned_individual(request, individual_id)
                individual.is_featured = False
                individual.save()
        if request.POST['selectionField'] == "Delete":
            for individual_id in individuals:
                individual = get_owned_individual(request, individual_id)


                individual_id = individual.id
                username = individual.user.username

                #delete files
                if individual.vcf_file:
                    individual.vcf_file.delete()
                # if individual.strs_file:
                #     individual.strs_file.delete()
                # if individual.cnvs_file:
                #     individual.cnvs_file.delete()
                shutil.rmtree(os.path.join(settings.BASE_DIR, 'genomes', username, str(individual_id)), ignore_errors=True)

                individual.delete()
            #os.system('rm -rf rockbio14/site_media/media/genomes/%s/%s' % (username, individual_id))
        if request.POST['selectionField'] == "Populate":
            for individual_id in individuals:
                individual = get_owned_individual(request, individual_id)
                PopulateVariants.delay(individual.id)
            
        if request.POST['selectionField'] == "Annotate":
            for individual_id in individuals:
                individual = get_owned_individual(request, individual_id)
                AnnotateVariants.delay(individual.id)
        if request.POST['selectionField'] == "Find_Medical_Conditions_and_Medicines":
            for individual_id in individuals:
                individual = get_owned_individual(request, individual_id)
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



    groups = owned_groups(request.user)
#    individuals = Individual.objects.annotate(number_of_variants=Count('variant'))
    
    
    return render(request, 'individuals/list.html', {'individuals': individuals, 'groups':groups, 'ind_featured':ind_featured})


@login_required
def annotate(request, individual_id):
    individual = get_owned_individual(request, individual_id)
    individual.status = 'new'
    individual.n_lines = 0
    VerifyVCF.delay(individual.id)
    individual.save()
    messages.add_message(request, messages.INFO, "Your individual is being annotated.")
    return redirect('dashboard')

@login_required
def populate(request, individual_id):
    individual = get_owned_individual(request, individual_id)
    PopulateVariants.delay(individual.id)
    messages.add_message(request, messages.INFO, "Your individual is being populated.")

    return redirect('dashboard')


@login_required
def populate_mongo(request, individual_id):
    individual = get_owned_individual(request, individual_id)
    PopulateMongoVariants.delay(individual.id)
    messages.add_message(request, messages.INFO, "Your individual is being inserted at MongoDB.")

    return redirect('individuals_list')


def download(request, individual_id):
    individual = get_owned_individual(request, individual_id)
    
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
    individual = get_owned_individual(request, individual_id)
    
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
    response['Content-Disposition'] = 'attachment; filename=%s.annotated.rockbio.vcf.zip' % basename
    response['Content-Length'] = os.path.getsize(fullpath)
    return response

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            
            return redirect('individuals_list')
    else:
        form = GroupForm(user=request.user)
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def view_group(request, group_id):
    group = get_object_or_404(owned_groups(request.user), pk=group_id)
    return render(request, 'groups/view_group.html', {'group': group})

class GroupDeleteView(DeleteView):
    model = Group

    def get_queryset(self):
        return owned_groups(self.request.user)

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
                variants_ind_one = owned_variants(request).filter(individual__id=individual_one_id, **query).values('chr', 'pos', 'genotype')
                
                variants_ind_two = owned_variants(request).filter(individual__id=individual_two_id, **query).values('chr', 'pos', 'genotype')
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


def _individual_storage_path(individual):
    if individual.user:
        username = slugify(individual.user.username)
    else:
        username = 'public'
    return os.path.join(settings.BASE_DIR, 'genomes', username, str(individual.id))


def _can_view_individual(request, individual):
    # Staff see everything; everyone else only their own samples.
    # Samples with no owner are staff-only (they used to be public).
    if request.user.is_staff:
        return True
    return request.user.is_authenticated and individual.user_id == request.user.id


def _read_tail(path, max_bytes=60000):
    if not os.path.exists(path):
        return ''
    with open(path, 'rb') as log_file:
        log_file.seek(0, os.SEEK_END)
        size = log_file.tell()
        log_file.seek(max(0, size - max_bytes))
        return log_file.read().decode('utf-8', errors='replace')


def annotation_monitor(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    if not _can_view_individual(request, individual):
        return HttpResponseForbidden()
    return render(request, 'individuals/annotation_monitor.html', {'individual': individual})


def annotation_status(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    if not _can_view_individual(request, individual):
        return HttpResponseForbidden()

    path = _individual_storage_path(individual)
    progress_path = os.path.join(path, 'annotation.progress.json')
    log_path = os.path.join(path, 'annotation.log')
    progress = {}
    if os.path.exists(progress_path):
        try:
            with open(progress_path) as progress_file:
                progress = json.load(progress_file)
        except ValueError:
            progress = {}
    has_log = os.path.exists(log_path)
    fallback_stage = individual.status or 'pending'
    fallback_message = ''
    if not has_log and individual.status == 'new':
        fallback_stage = 'not_started'
        fallback_message = 'Annotation has not been queued yet. Click Start annotation.'

    data = {
        'id': individual.id,
        'name': individual.name,
        'status': individual.status,
        'annotation_time': str(individual.annotation_time or ''),
        'n_variants': individual.n_variants,
        'stage': progress.get('stage') or fallback_stage,
        'percent': progress.get('percent'),
        'message': progress.get('message') or fallback_message,
        'updated_at': progress.get('updated_at') or '',
        'log': _read_tail(log_path),
        'has_log': has_log,
    }
    return DjangoJsonResponse(data)
