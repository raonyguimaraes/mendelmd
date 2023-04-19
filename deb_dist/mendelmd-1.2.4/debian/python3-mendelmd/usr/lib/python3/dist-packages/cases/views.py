from django.shortcuts import render
from django.shortcuts import redirect
from django.template import RequestContext
from .forms import CaseForm
from cases.models import Case
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.views.generic import CreateView, DeleteView

from individuals.models import Individual
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required
def cases_list(request):

    if request.user.is_staff:
        cases = Case.objects.all().order_by('id')
    else:
        cases = Case.objects.filter(user=request.user).order_by('id')

    context = {'cases': cases}

    return render(request, 'cases/list.html', context)


@login_required
def create_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES)        
        if form.is_valid():            
            case = form.save(commit=False)
            case.user = request.user
            case.save()
            form.save_m2m()
            return redirect('cases_list')
    else:
        form = CaseForm()
    return render(request, 'cases/new.html', {'form': form})

@login_required
def view_case(request, case_id):

    if request.user.is_staff:
        case = get_object_or_404(Case, pk=case_id)
    else:
        case = get_object_or_404(Case, pk=case_id, user=request.user)

    return render(request, 'cases/view.html', {'case': case})


class CaseDeleteView(LoginRequiredMixin, DeleteView):

    model = Case

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        
        self.object.delete()
        messages.add_message(request, messages.INFO, "Case deleted with success!")
        return redirect('cases_list')
    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects


    
@login_required
def edit(request, case_id):
    
    if request.user.is_staff:
        case = get_object_or_404(Case, pk=case_id)
    else:
        case = get_object_or_404(Case, pk=case_id, user=request.user)

        
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES, instance=case)        
        if form.is_valid():
            form.save()
#            variants = form.cleaned_data['variants']
#            strs = form.cleaned_data['strs']
#            cnvs = form.cleaned_data['cnvs']
#            #use id for unique names
#            individual = Individual.objects.create(user=request.user, status='new')
#            
#            individual.variants=variants
#            individual.strs=cnvs
#            individual.cnvs=cnvs
#            
#            individual.name=request.POST['name']
#            individual.save()
#            AnnotateVariants.delay(individual.id)
            return redirect('cases_list')
    else:
        form = CaseForm(instance=case)
    return render(request, 'cases/edit.html', {'form': form})

@login_required
def analysis(request, case_id, analysis, inheritance):
    
    if request.user.is_staff:
        case = get_object_or_404(Case, pk=case_id)
    else:
        case = get_object_or_404(Case, pk=case_id, user=request.user)
        
    query_string = []
    query_string.append('variants_per_gene=')

    query_string.append('impact=HIGH')
    query_string.append('impact=MODERATE')
    query_string.append('dbsnp_option=>')
    query_string.append('dbsnp_build=130')
    query_string.append('read_depth_option=>')
    query_string.append('read_depth=10')
    # query_string.append('')
    query_string.append('genomes1000=0+-+0.005')
    query_string.append('dbsnp_frequency=0+-+0.005')
    query_string.append('esp_frequency=0+-+0.005')

    
    if analysis == 'filter_analysis':
        query_string.append('genes_in_common=on')

    if analysis == 'filter_analysis' or analysis == 'pathway_analysis' :

        #add children and cases to individuals
        for individual in case.children.all():
            query_string.append('individuals=%s' % (individual.id))
        for individual in case.cases.all():
            query_string.append('individuals=%s' % (individual.id))
        for individual in case.controls.all():
            query_string.append('exclude_individuals=%s' % (individual.id))

        #add father and mother to exclude individuals
        if case.father:
            query_string.append('exclude_individuals=%s' % (case.father.id))
        if case.mother:
            query_string.append('exclude_individuals=%s' % (case.mother.id))
        
        
        # filterstring = "&".join(query_string)
        # return redirect(reverse('filter_analysis')+'?'+filterstring)

    if analysis == 'family_analysis':
        query_string.append('genes_in_common=on')

        query_string.append('remove_not_in_parents=on')

        if case.father:
            query_string.append('father=%s' % (case.father.id))
        if case.mother:
            query_string.append('mother=%s' % (case.mother.id))
        for individual in case.children.all():
            query_string.append('children=%s' % (individual.id))
        for individual in case.cases.all():
            query_string.append('individuals=%s' % (individual.id))
        for individual in case.controls.all():
            query_string.append('exclude_individuals=%s' % (individual.id))



        if inheritance == 'recessive_homozygous':
            query_string.append('inheritance_option=1')
        if inheritance == 'dominant_heterozygous':
            query_string.append('inheritance_option=2')
        if inheritance == 'compound_heterozygous':
            query_string.append('inheritance_option=3')
        if inheritance == 'x_linked':
            query_string.append('chr=X')
            query_string.append('inheritance_option=2')

    #inheritance
    if inheritance == 'recessive_homozygous':        
        query_string.append('mutation_type=homozygous')
    if inheritance == 'compound_heterozygous':        
        query_string.append('mutation_type=heterozygous')
        query_string.append('variants_per_gene_option=>')
        query_string.append('variants_per_gene=2')
    if inheritance == 'dominant_heterozygous':        
        query_string.append('mutation_type=heterozygous')
    if inheritance == 'x_linked':        
        query_string.append('mutation_type=homozygous')
        query_string.append('chr=X')


    #join all options
    filterstring = "&".join(query_string)

    if analysis == 'filter_analysis':
        url_redirect = 'filter_analysis'
    if analysis == 'family_analysis':
        url_redirect = 'family_analysis'
    if analysis == 'pathway_analysis':
        url_redirect = 'pathway_filter_analysis'
    
    return redirect(reverse(url_redirect)+'?'+filterstring)