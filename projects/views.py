from django.shortcuts import render, redirect, get_object_or_404

from .models import Project
from .forms import ProjectForm

# Create your views here.
def index(request):
    projects = Project.objects.all()
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
