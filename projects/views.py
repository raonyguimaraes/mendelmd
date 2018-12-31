from django.shortcuts import render, redirect, get_object_or_404

from .models import Project
from files.models import File

from tasks.models import Task

from .forms import ProjectForm, ImportForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy

from tasks.tasks import run_qc
from files.tasks import check_file

from .tasks import import_project_files_task

from settings.models import S3Credential

import boto3
import os

from .models import ProjectFile, ProjectSample


from django.utils.decorators import method_decorator

from django.core import serializers

@login_required
def index(request):

    if request.user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(user=request.user)

    context = {'projects':projects}
    return render(request, 'projects/index.html', context)

@login_required
def create(request):
    """
    Create Project
    """
    form = ProjectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()

            return redirect('projects-view', project_id=project.id)

    context = {'form': form}
    return render(request, 'projects/create.html', context)

@method_decorator(login_required, name='dispatch')
class ProjectUpdate(UpdateView):
    model = Project
    fields = ['name', 'paths']

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects

@login_required
def view(request, project_id):

    if request.user.is_staff:
        project = get_object_or_404(Project, pk=project_id)
    else:
        project = get_object_or_404(Project, pk=project_id, user=request.user)

    print(dir(project))

    n_files = project.files.count()
    n_samples = project.files.count()
    # total_file_size = 0
    # total_file_size = sum(project.files.values_list('size', flat=True))
    
    context = {
        'project': project,
        'n_files':n_files,
        'n_samples':n_samples,
        # 'total_file_size':total_file_size,
    }

    return render(request, 'projects/view.html', context)

@login_required
def project_files(request, project_id):

    if request.user.is_staff:
        project = get_object_or_404(Project, pk=project_id)
    else:
        project = get_object_or_404(Project, pk=project_id, user=request.user)

    n_files = project.projectfile_set.count()

    context = {
        'project': project,
        'n_files':n_files
    }
    
    return render(request, 'projects/project_files.html', context)


@login_required
def import_files(request, project_id):
    if request.user.is_staff:
        project = get_object_or_404(Project, pk=project_id)
    else:
        project = get_object_or_404(Project, pk=project_id, user=request.user)

    form = ImportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # paths = form.cleaned_data['paths']

            for file in form.cleaned_data['file_list'].splitlines():
                
                try:
                    obj = File.objects.get(location=file, user=request.user)
                except File.DoesNotExist:
                    obj = File(location=file, user=request.user)
                    obj.save()
                    project.files.add(obj)

            # for path in form.cleaned_data['paths'].splitlines():
                
            #     clean_path = path.strip().replace('s3://', '')
            #     split_path = clean_path.split('/', 1)
            #     bucket_name = split_path[0]
            #     prefix = split_path[1]

            #     s3credentials = S3Credential.objects.all()
            #     for s3credential in s3credentials:
            #         if clean_path.startswith(s3credential.buckets):
            #             #get all files from path
            #             session = boto3.Session(
            #                 aws_access_key_id=s3credential.access_key,
            #                 aws_secret_access_key=s3credential.secret_key
            #             )
            #             s3 = session.resource('s3')
            #             bucket = s3.Bucket(bucket_name)
            #             print(bucket)
            #             for key in bucket.objects.filter(Prefix=prefix):
                            

            #                 if not key.key.endswith('/'):
            #                     file_name, file_extension = os.path.splitext(key.key)
            #                     if file_extension == '.gz':
            #                         file_name, file_extension = os.path.splitext(file_name)
                                
            #                     basename = os.path.basename(file_name)
            #                     location = 's3://'+bucket_name+'/'+key.key

            #                     file_obj = ProjectFile(
            #                         project = project,
            #                         name=basename,
            #                         size=str(key.size),
            #                         last_modified=str(key.last_modified),
            #                         file_type=file_extension.replace('.', ''),
            #                         location=location,
            #                         user=request.user
            #                     )

            #                     file_obj.save()

            for sample_info in form.data['samples'].splitlines():
                sample_info = sample_info.split('\t')

                sample = ProjectSample(user=request.user, project=project)
                
                sample.name = sample_info[0]
                sample.alias = sample_info[1]
                sample.status = sample_info[2]
                sample.location = sample_info[3]
                sample.prefix = sample_info[4]
                sample.save()

            return redirect('projects-view', project.id)
    context = {'form': form, 'project': project}
    return render(request, 'projects/import_files.html', context)

@method_decorator(login_required, name='dispatch')
class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projects-index')

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects

@login_required
def import_project_files(request, project_id):
    project = Project.objects.get(pk=project_id)
    if project.user == request.user:
        import_project_files_task.delay(project_id)
    return redirect('projects-view', project_id=project_id)


@login_required
def bulk_action(request, project_id):

    if request.user.is_staff:
        project = get_object_or_404(Project, pk=project_id)
    else:
        project = get_object_or_404(Project, pk=project_id, user=request.user)

    if request.method == 'POST':
        
        action = request.POST['action']

        # print('POST', request.POST)

        model = request.POST['model']


        if model == 'files':
    
            files = request.POST.getlist('files')


            if action == 'analysis':

                request.session['files'] = files
                request.session['project_id'] = project_id
                
                return redirect('analysis-create')


            for file_id in files:
                file = File.objects.get(pk=file_id)
                if action == "delete":
                    file.delete()
                if action == "qc":
                    if file.file_type in ['fq', 'fastq', 'bam', 'vcf']:
                        task = Task()
                        task.name = 'QC ProjectFile %s' % (file.id)
                        task.type = 'qc'
                        task.action = 'qc'
                        task.status = 'new'
                        task.manifest = {
                            'input':file.location,
                            'project':project.id,
                            'file':file.id,
                            'type':'qc',
                        }
                        task.save()
                        run_qc.delay(task.id)
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







        if model == 'samples':
            samples = request.POST.getlist('samples')
            for sample_id in samples:
                sample = ProjectSample.objects.get(pk=sample_id)
                if action == "delete":
                    sample.delete()

            
    return redirect('projects-view', project_id=project_id)
