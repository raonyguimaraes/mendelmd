
from django.forms import ModelForm
from individuals.models import *
from django import forms
from variants.models import *


class IndividualForm(ModelForm):


    vcf_file = forms.CharField(max_length=600, required=False)

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

    def __init__(self, user=None, *args, **kwargs):
        
        super(ComparisonForm, self).__init__(*args, **kwargs)

        if user.is_staff:
            
            self.fields['individual_one'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False)
            self.fields['individual_two'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False)

        elif not user.is_authenticated:
            
            self.fields['individual_one'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=None).order_by('id'), required=False)
            self.fields['individual_two'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=None).order_by('id'), required=False)
        else:
            print('user', user)
            self.fields['individual_one'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=user).order_by('id'), required=False)
            self.fields['individual_two'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=user).order_by('id'), required=False)
    

            
class BrowserForm(forms.Form):
    
    chr = forms.CharField(max_length=50, required=False)
    pos = forms.CharField(max_length=50, required=False)
    
    snp_id = forms.CharField(max_length=50, required=False)
    snp_list = forms.CharField(widget=forms.Textarea, required=False)
    
    gene = forms.CharField(max_length=50, required=False)
    gene_list = forms.CharField(widget=forms.Textarea, required=False)

    CHOICES = [(x, x.replace('_', ' ')) for x in ['CDS', 'CHROMOSOME_LARGE DELETION', 'CODON_CHANGE', 'CODON_INSERTION', 'CODON_CHANGE_PLUS CODON_INSERTION', 'CODON_DELETION', 'CODON_CHANGE_PLUS CODON_DELETION', 'DOWNSTREAM', 'EXON', 'EXON_DELETED', 'FRAME_SHIFT', 'GENE', 'INTERGENIC', 'INTERGENIC_CONSERVED', 'INTRAGENIC', 'INTRON', 'INTRON_CONSERVED', 'MICRO_RNA', 'NON_SYNONYMOUS_CODING', 'NON_SYNONYMOUS_START', 'NON_SYNONYMOUS_STOP', 'RARE_AMINO_ACID', 'SPLICE_SITE_ACCEPTOR', 'SPLICE_SITE_DONOR', 'SPLICE_SITE_REGION', 'SPLICE_SITE_BRANCH', 'SPLICE_SITE_BRANCH_U12', 'STOP_LOST', 'START_GAINED', 'START_LOST', 'STOP_GAINED', 'SYNONYMOUS_CODING', 'SYNONYMOUS_START', 'SYNONYMOUS_STOP', 'TRANSCRIPT', 'REGULATION', 'UPSTREAM', 'UTR_3_PRIME', 'UTR_3_DELETED', 'UTR_5_PRIME', 'UTR_5_DELETED']]
    
    snp_eff = forms.MultipleChoiceField(choices=CHOICES, required=False)

    # CHOICES = [(x[0], x[0]) for x in Variant.objects.values_list('snpeff_func_class').distinct()]

    CHOICES = [(x, x.replace('_', ' ')) for x in ['NONE', 'SILENT', 'MISSENSE', 'NONSENSE']]

    func_class = forms.MultipleChoiceField(choices=CHOICES, required=False)
    
    CHOICES = [(x, x.replace('_', ' ')) for x in ['HIGH', 'MODERATE', 'MODIFIER', 'LOW']]

    impact = forms.MultipleChoiceField(choices=CHOICES, required=False)
    
    cln = forms.BooleanField(required=False)
