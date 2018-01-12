from django.shortcuts import render

from .models import Analysis
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from django.shortcuts import render
from formtools.wizard.views import SessionWizardView



# Create your views here.
def index(request):
    print('Hello World')
    analyses = Analysis.objects.all()

    context = {'analyses': analyses}

    return render(request, 'analyses/index.html', context)

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

class ContactWizard(SessionWizardView):
    def done(self, form_list, **kwargs):

        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })