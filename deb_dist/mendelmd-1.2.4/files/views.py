from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.management import call_command

from files.models import File
from django.contrib.auth.decorators import login_required

from tasks.tasks import compress_file
from .tasks import check_file
from tasks.models import Task

from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404, redirect
from collections import Counter
from django.db.models import Q

from django.http import HttpResponse
#for upload
from .forms import UploadForm
from django.utils.text import slugify
import os
from django.conf import settings
import json

# from .forms import FileForm


@login_required
def index(request):

    query  = ''
    args = []

    if request.method == 'POST':

        # form = FileForm(request.POST)
        # if form.is_valid():
        #     pass

        # print(request.POST)
        files = request.POST.getlist('files')
        action = request.POST['action']
        query = request.POST['query']
        order_string ='sample'
        # print('query', query)
        if action == 'analysis':
            request.session['files'] = files
            return redirect('analysis-create')
        
        for file_id in files:

            # file = File.objects.get(pk=file_id)
            if request.user.is_staff:
                file = get_object_or_404(File, pk=file_id)
            else:
                file = get_object_or_404(File, pk=file_id, user=request.user)

            if action == "delete":
                file.delete()
            else:
                task_manifest = {}
                task_manifest['file'] = file.id
                task_manifest['action'] = action
                task = Task(user=request.user)
                
                task.manifest = task_manifest
                task.status = 'new'
                task.action = action
                task.user = request.user
                task.save()

                if action == "check":
                    check_file.delay(task.id)                
                if action == "compress":
                    compress_file.delay(task.id)
                file.status = 'scheduled'
                file.save()

        status = request.POST.getlist('status')
        
        print('status', status)

        if len(status[0]) > 0:
            args.append(Q(status__in=status))

        extension = request.POST.getlist('extension')

        if len(extension[0]) > 0:
            print('extension',extension)
            args.append(Q(extension__in=extension))

        print('args', args)

    else:
        # form = FileForm()
        print(request.GET)
        if 'orderby' in request.GET:
            orderby = request.GET['orderby']
            order = request.GET['order'][0]
            if order == 'desc':
                order_string = '-{}'.format(orderby)
            else:
                order_string = orderby
        else:
            order_string = 'name'

    # print(order_string, 'order_string')
    
    if request.user.is_staff:#status='scheduled' size=0
        # files = File.objects.filter(location__icontains=query, *args).order_by(order_string)#size
        files = File.objects.filter(location__regex=query, *args).order_by(order_string)#size
        
    else:
        files = File.objects.filter(user=request.user).order_by(order_string)
    #sample__isnull=True
    # files = File.objects.filter(*args).order_by('-id')

    files_summary = {}
    files_summary['status'] = dict(Counter(files.values_list('status', flat=True)))
    files_summary['file_type'] = dict(Counter(files.values_list('file_type', flat=True)))
    files_summary['extension'] = dict(Counter(files.values_list('extension', flat=True)))
    # files_summary['total_size'] = sum(files.values_list('size', flat=True))
    # files_summary = 0
    filetypes = []
    n_files = []
    for filetype in files_summary['extension']:
        # print(filetype, files_summary['extension'][filetype])
        filetypes.append(filetype)
        n_files.append(files_summary['extension'][filetype])
    files_summary['filetypes'] = filetypes
    files_summary['n_files'] = n_files


    context = {
        # 'form': form,
        'query':query,
        'files':files,
        'n_files':len(files),
        'files_summary':files_summary
    }

    return render(request, 'files/index.html', context)

@login_required
def view(request, file_id):

    file = File.objects.get(pk=file_id)
    print(dir(file))
    context = {
    'file':file
    }
    return render(request, 'files/view.html', context)


@login_required
def import_files(request):
    print('Hello World')
    
    # 


    return redirect('files-index')

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

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            if request.user.is_authenticated:
                file = File.objects.create(user=request.user, status='new')
            else:
                file = File.objects.create(user=None, status='new')

            file.local_file = request.FILES.get('file')
            
            print('file')
            print(request.FILES.get('file'))

            filename = file.local_file.name.split('.')
            new_filename = []
            for tag in filename:
                new_filename.append(slugify(tag))

            file.local_file.name = ".".join(new_filename)

            

            # print('file.location ', file.location)

            #get name from inside vcf file
            #clean this...
            file.name= str(os.path.splitext(file.local_file.name)[0]).replace('.vcf','').replace('.gz','').replace('.rar','').replace('.zip','').replace('._',' ').replace('.',' ')

            # file.shared_with_groups = form.cleaned_data['shared_with_groups']
            # file.shared_with_groups.set(form.cleaned_data['shared_with_groups'])
            
            file.save()
            
            f = file.local_file

            #fix permissions
            #os.chmod("%s/genomes/%s/" % (settings.BASE_DIR, file.user), 0777)

            if request.user.is_authenticated:
                file_path = "%s/media/%s/%s" % (settings.BASE_DIR, slugify(file.user), file.id)
            else:
                file_path = "%s/media/public/%s" % (settings.BASE_DIR, file.id)
            os.chmod(file_path, 0o777)

            file.location = '/'+file.local_file.url

            # AnnotateVariants.delay(file.id)
            
            task_manifest = {}
            task_manifest['file'] = file.id
            task_manifest['action'] = 'check'
            task = Task(user=request.user)
            
            task.manifest = task_manifest
            task.status = 'new'
            task.action = 'check'
            task.save()

            check_file.delay(task.id)

            file.status = 'scheduled'
            file.save()

            data = {'files': [{'deleteType': 'DELETE', 'name': file.name, 'url': '', 'thumbnailUrl': '', 'type': 'image/png', 'deleteUrl': '', 'size': f.size}]}

            response = JSONResponse(data, mimetype=response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            print(form.errors)

    else:
        form = UploadForm()

    return render(request, 'files/upload.html', {'form':form})


class FileUpdate(LoginRequiredMixin, UpdateView):
    model = File
    fields = '__all__'

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects

class FileDelete(LoginRequiredMixin, DeleteView):
    model = File
    success_url = reverse_lazy('files-index')
    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects

@login_required
def bulk_action(request):

    if request.method == 'POST':
        files = request.POST.getlist('files')
        action = request.POST['action']

        for file_id in files:


            # file = File.objects.get(pk=file_id)
            if request.user.is_staff:
                file = get_object_or_404(File, pk=file_id)
            else:
                file = get_object_or_404(File, pk=file_id, user=request.user)

            if action == "delete":
                file.delete()
            if action == "check":
                
                task_manifest = {}
                task_manifest['file'] = file.id
                task_manifest['action'] = action
                task = Task(user=request.user)
                
                task.manifest = task_manifest
                task.status = 'new'
                task.action = action
                task.user = request.user
                task.save()

                check_file.delay(task.id)

                file.status = 'scheduled'
                file.save()

    return redirect('files-index')

@login_required
def run_task(request):
    if request.method == 'GET':
        print(request.GET)
        if 'action' in request.GET:
            action = request.GET['action']
            file_id  = request.GET['file_id']

            file = File.get_object_or_404(pk=file_id)
            if action == "check":
                
                task_manifest = {}
                task_manifest['file'] = file.id
                task_manifest['action'] = action
                task = Task(user=request.user)
                
                task.manifest = task_manifest
                task.status = 'new'
                task.action = action
                task.user = request.user
                task.save()

                check_file.delay(task.id)

                file.status = 'scheduled'
                file.save()
            
    return redirect('files-index')

@login_required
def run_task(request):
    if request.method == 'GET':
        print(request.GET)
        if 'action' in request.GET:
            action = request.GET['action'][0]
            file_id  = request.GET['file_id'][0]
            print(action, file_id)
    return redirect('files-index')