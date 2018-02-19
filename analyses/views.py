from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404


from .models import Analysis
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from tasks.tasks import run_qc
from .tasks import create_analysis_tasks

from projects.models import Project
from files.models import File
from .forms import CreateAnalysis
from tasks.models import Task
from samples.models import SampleGroup
from django.utils.html import strip_tags

# Create your views here.
def index(request):

    query  = ''
    args = []

    if request.method == 'POST':
        
        analyses = request.POST.getlist('analyses')
        action = request.POST['action']
        query = request.POST['query']
        # print('query', query)
        for analysis_id in analyses:

            # file = File.objects.get(pk=file_id)
            if request.user.is_staff:
                analysis = get_object_or_404(Analysis, pk=analysis_id)
            else:
                analysis = get_object_or_404(Analysis, pk=analysis_id, user=request.user)

            if action == "delete":
                analysis.delete()

    print('Hello World')
    analyses = Analysis.objects.all()

    context = {'analyses': analyses}

    return render(request, 'analyses/index.html', context)

def create(request):
    params = {}
    
    if 'files' in request.session:
        file_list = request.session['files']
        files = File.objects.filter(pk__in=file_list)
    else:
        file_list = None
        files = None

    files = File.objects.all()

    if 'project_id' in request.session:

        project_id = request.session['project_id']
        project = Project.objects.get(pk=project_id)
    else:
        project = None

    if request.method == 'POST':
        
        form = CreateAnalysis(request.POST)
        print(request.POST)
        
        if form.is_valid():

            analysis = Analysis(user=request.user)
            
            analysis.name = form.cleaned_data['name']
            

            # analysis.files = form.cleaned_data['files']

            # analysis.analysis_types = form.cleaned_data['analysis_types']
            params['providers'] = form.cleaned_data['providers']
            params['analysis_types'] = form.cleaned_data['analysis_types']
            params['files'] = strip_tags(form.cleaned_data['files'].replace('<br>', '\n')).strip().split('\n')
            
            

            # file_list#
            analysis.status = 'new'
            analysis.project = project
            analysis.params = params

            analysis.save()

            create_analysis_tasks.delay(analysis.id)

            # task_manifest = params
            # task = Task(user=request.user)
            # task.manifest = task_manifest
            # task.status = 'new'
            # task.action = 'analysis'
            # task.save()

            return redirect('analysis-detail', analysis.id)
            
    else:
        form = CreateAnalysis()
    
    # print(file)
    # print(project.name)

    # if request.POST:
        # params = request.POST['params']
        # print(params)

    context = {
        'project': project,
        # 'files': files,
        'form':form,
        }

    return render(request, 'analyses/create.html', context)


class AnalysisDelete(DeleteView):
    model = Analysis
    success_url = reverse_lazy('analyses-index')

# class AnalysisCreate(CreateView):
#     model = Analysis
#     fields = ['name']

class AnalysisUpdate(UpdateView):
    model = Analysis
    fields = ['name', 'params']

class AnalysisDetailView(DetailView):
    model = Analysis
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # print('params', self.object.params)
        files = []
        if 'sample_groups' in self.object.params:
            # for group in self.object.params['sample_groups']:
                # files = File.objects.filter()
                sample_groups = self.object.params['sample_groups']
                samples = SampleGroup.objects.filter(pk__in=sample_groups).values_list('members', flat=True)
                # print('samples', samples)
                context['files'] = File.objects.filter(sample__in=samples)
                # print(context['files'])
        if 'files' in self.object.params:
            files = self.object.params['files']
            # context['files'] = File.objects.filter(pk__in=files)
        context['tasks'] = Task.objects.filter(analysis=self.object)

        context['output_files'] = File.objects.filter(task__in=context['tasks'])
        print(len(context['output_files']))
        # for file in context['output_files']:
        #     print(dir(file))
            
        return context

def human_size(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    """ Returns a human readable string reprentation of bytes"""
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])

def run_analysis(request, analysis_id):
    
    print('run analysis')
    create_analysis_tasks.delay(analysis_id)

    return redirect('analysis-detail', analysis_id)
    


class ContactWizard(SessionWizardView):
    def done(self, form_list, **kwargs):

        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
