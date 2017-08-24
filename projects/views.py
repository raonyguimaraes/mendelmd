from django.shortcuts import render, redirect, get_object_or_404

from .models import Project
from .forms import ProjectForm, ImportFilesForm
from files.models import File
# Create your views here.
def index(request):
    projects = Project.objects.all()
    for project in projects:
        project.n_files = project.files.count()
    context = {'projects':projects}
    return render(request, 'projects/index.html', context)

def create(request):
    """
    Create Project
    """
    form = ProjectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('projects-index')

    context = {'form': form}
    return render(request, 'projects/create.html', context)

def view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {'project': project}
    return render(request, 'projects/view.html', context)

def import_files(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ImportFilesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            for file in form.cleaned_data['file_list'].splitlines():
                # print(file)
                file_objs = File.objects.filter(name__contains=file)
                # print(file_obj)
                for file_obj in file_objs:
                    project.files.add(file_obj)
            # form.save()
            return redirect('projects-view', project.id)

    context = {'form': form, 'project': project}
    return render(request, 'projects/import_files.html', context)