from django.shortcuts import render, redirect, get_object_or_404

from .models import Project, File, Path
from .forms import ProjectForm, ImportForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    projects = Project.objects.all()
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
            form.save()
            return redirect('projects-index')

    context = {'form': form}
    return render(request, 'projects/create.html', context)

@login_required
def view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {'project': project}
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

            # for file in form.cleaned_data['file_list'].splitlines():
            #     file_obj = File(location=file)
            #     file_obj.save()
            #     project.files.add(file_obj)
            return redirect('projects-view', project.id)
    context = {'form': form, 'project': project}
    return render(request, 'projects/import_files.html', context)