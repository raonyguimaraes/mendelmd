from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404


from .models import Analysis
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from .tasks import run_analysis_task

from projects.models import Project
from files.models import File
from .forms import CreateAnalysis

# Create your views here.
def index(request):
    print('Hello World')
    analyses = Analysis.objects.all()

    context = {'analyses': analyses}

    return render(request, 'analyses/index.html', context)

def create(request):
    params = {}
    file_list = request.session['files']

    files = File.objects.filter(pk__in=file_list)

    project_id = request.session['project_id']

    project = Project.objects.get(pk=project_id)

    if request.method == 'POST':
        
        form = CreateAnalysis(request.POST)
        print(request.POST)
        
        if form.is_valid():

            analysis = Analysis(user=request.user)
            
            analysis.name = form.cleaned_data['name']
            

            # analysis.files = form.cleaned_data['files']

            # analysis.analysis_types = form.cleaned_data['analysis_types']
            params['analysis_types'] = form.cleaned_data['analysis_types']
            params['files'] = file_list#form.cleaned_data['files']
            analysis.project = project
            analysis.params = params

            analysis.save()

            return redirect('analysis-detail', analysis.id)
            
    else:
        form = CreateAnalysis()
    
    # print(file)
    print(project.name)

    # if request.POST:
        # params = request.POST['params']
        # print(params)

    context = {
        'project': project,
        'files': files,
        'form':form,
        }

    return render(request, 'analyses/create.html', context)


class AnalysisDelete(DeleteView):
    model = Analysis
    success_url = reverse_lazy('analyses-index')

class AnalysisCreate(CreateView):
    model = Analysis
    fields = ['name']

class AnalysisUpdate(UpdateView):
    model = Analysis
    fields = ['name']

class AnalysisDetailView(DetailView):
    model = Analysis

def run_analysis(request, analysis_id):
    
    print('run analysis')
    run_analysis_task.delay(analysis_id)

    return redirect('analysis-detail', analysis_id)
    


class ContactWizard(SessionWizardView):
    def done(self, form_list, **kwargs):

        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })