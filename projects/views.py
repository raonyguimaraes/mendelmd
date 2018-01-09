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

from tasks.tasks import import_project_files_task, check_file


@login_required
def index(request):

    if request.user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.all(user=request.user)

    # for project in projects:
    #     project.n_files = project.files.count()
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
            project = form.save()

            return redirect('projects-view', project_id=project.id)

    context = {'form': form}
    return render(request, 'projects/create.html', context)

class ProjectUpdate(UpdateView):
    model = Project
    fields = ['name', 'paths']

@login_required
def view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {'project': project}
    # print(project.files.all)
    return render(request, 'projects/view.html', context)

@login_required
def import_files(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ImportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            path = form.cleaned_data['path']
            # if path.startswith('s3://'):
                #get files form s3 and add to project

            for file in form.cleaned_data['file_list'].splitlines():
                
                try:
                    obj = File.objects.get(location=file, user=request.user)
                except File.DoesNotExist:
                    obj = File(location=file, user=request.user)
                    obj.save()
                    project.files.add(obj)

            return redirect('projects-view', project.id)
    context = {'form': form, 'project': project}
    return render(request, 'projects/import_files.html', context)

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projects-index')

def import_project_files(request, project_id):
    
    print('Import Stuff')
    import_project_files_task.delay(project_id)
    return redirect('projects-view', project_id=project_id)


@login_required
def bulk_action(request, project_id):
    if request.method == 'POST':
        files = request.POST.getlist('files')
        action = request.POST['action']
        task_manifest = {}

        for file in files:
            
            task_manifest = {}
            task_manifest['file'] = file
            task_manifest['action'] = action
            task = Task(user=request.user)
            task.manifest = task_manifest
            
            task.status = 'new'
            task.action = action
            task.user = request.user
            task.save()

            if action == "check":
                task.name = 'check file'
                check_file.delay(task.id)
            if action == "download":
                task.name = 'download file'
                download_file.delay(task.id)
            
            task.save()

    return redirect('projects-view', project_id=project_id)
