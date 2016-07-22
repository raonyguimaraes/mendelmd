
from django.forms import ModelForm
from individuals.models import *
from django import forms
from variants.models import *


class IndividualForm(ModelForm):
    class Meta:
        model = Individual
        fields = '__all__'
        #'user', 'shared_with_users', , 'is_featured', 'is_public', 'vcf_file', 'vcf_header', 'status', 'n_variants', 'n_lines', 'creation_date', 'modified_date', 'annotation_time', 'insertion_time', 'insertion_time_mongo'

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class ControlGroupForm(ModelForm):
    class Meta:
        model = ControlGroup
        fields = '__all__'


class ComparisonForm(forms.Form):

    individual_one = forms.ModelChoiceField(queryset=Individual.objects.all().order_by('id'), required=False)
    individual_two = forms.ModelChoiceField(queryset=Individual.objects.all().order_by('id'), required=False)
    # individual_two = forms.ChoiceField(choices=[(x.id, x.name) for x in Individual.objects.all()], required=False)
    read_depth = forms.CharField(max_length=50, required=False, label="Read Depth")
    

            
class BrowserForm(forms.Form):
    
    chr = forms.CharField(max_length=50, required=False)
    pos = forms.CharField(max_length=50, required=False)
    
    snp_id = forms.CharField(max_length=50, required=False)
    snp_list = forms.CharField(widget=forms.Textarea, required=False)
    
    gene = forms.CharField(max_length=50, required=False)
    gene_list = forms.CharField(widget=forms.Textarea, required=False)
    
    snp_eff = forms.MultipleChoiceField(choices=[(x[0], x[0]) for x in Variant.objects.values_list('snpeff_effect').distinct()], required=False)
    CHOICES = [(x[0], x[0]) for x in Variant.objects.values_list('snpeff_func_class').distinct()]
    func_class = forms.MultipleChoiceField(choices=CHOICES, required=False)
    
    impact = forms.MultipleChoiceField(choices=[(x[0], x[0]) for x in Variant.objects.values_list('snpeff_impact').distinct()], required=False)
    cln = forms.BooleanField(required=False)
