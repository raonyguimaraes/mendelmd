from django import forms

from individuals.models import *
from variants.models import *

from diseases.models import Disease, HGMDPhenotype

from filter_analysis.models import * 
from genes.models import *

from django.forms import ModelForm

# from django_select2 import *

from django.core.exceptions import ValidationError

from django_select2.forms import (HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget, ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget, Select2Widget)

from django.db.models import Q

def validate_fail_always(value):
    raise ValidationError('%s not valid. Infact nothing is valid!' % value)


# class MultiOmimChoices(ModelSelect2MultipleWidget):
#     queryset = Disease
#     search_fields = ['name__icontains', ]

class MultiOmimChoices(ModelSelect2Widget):
    model = Disease
    search_fields = [
        'name__icontains'
    ]
    def label_from_instance(self, obj):
        return force_text(obj.name).upper()

# class MultiHgmdChoices(AutoModelSelect2MultipleField):
#     queryset = HGMDPhenotype.objects
#     search_fields = ['name__icontains', ]
# class MultiCgdChoices(AutoModelSelect2MultipleField):
#     queryset = CGDCondition.objects
#     search_fields = ['name__icontains', ]
# class MultiCgdManifestationChoices(AutoModelSelect2MultipleField):
#     queryset = Manifestation.objects
#     search_fields = ['name__icontains', ]



# Create the form class.
class Filter(ModelForm):
     class Meta:
         model = FilterAnalysis
         fields = '__all__'

class FamilyFilter(ModelForm):
    class Meta:
        model = FamilyFilterAnalysis
        fields = '__all__'


#GENE_GROUPS= [(x.id, x.name) for x in GeneGroup.objects.all()]
FIELDS = Variant()._meta.get_fields()

class FilterAnalysisForm(forms.Form):
#    snp_id = forms.CharField(max_length=50, required=False)
    chr = forms.CharField(max_length=50, required=False, label='CHR')
    pos = forms.CharField(max_length=50, required=False, label='POS')
    
    snp_list = forms.CharField(widget=forms.Textarea, required=False, label='SNP LIST')
    exclude_snp_list = forms.CharField(widget=forms.Textarea, required=False, label='EXCLUDE SNP LIST')
    
    #individuals = forms.MultipleChoiceField(choices=[(x.id, x.name) for x in Individual.objects.filter().order_by('id')], required=False)

    # NUMBER_CHOICES = ['1', '2', '3', '4']
    # number = forms.ChoiceField(widget=Select2Widget, choices=NUMBER_CHOICES, required=False)


    individuals = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        queryset=Individual.objects.all().order_by('id'),
        search_fields=['name__icontains'],
    ), queryset=Individual.objects.all().order_by('id'), required=True)

    # individuals = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False, label='INDIVIDUALS')

    exclude_individuals = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False, label='EXCLUDE INDIVIDUALS')

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all().order_by('id'), required=False, label='GROUPS')
    exclude_groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all().order_by('id'), required=False, label='EXCLUDE GROUPS')

    
    # CHOICES = (('', ''),
    #            ('recessive', 'recessive'),
    #            ('dominant', 'dominant'),
    #            )
    # inheritance_model = forms.ChoiceField(required=False, choices=CHOICES, label="Inheritance Model")
    CHOICES = (('', ''),
               ('homozygous', 'HOMOZYGOUS  (Ex. 1/1, 2/1, 1/2)'),
               ('heterozygous', 'HETEROZYGOUS  (Ex. 0/1, 0/2, 1/0, 2/0)'),
               )
    mutation_type = forms.ChoiceField(required=False, choices=CHOICES, label="MUTATION TYPE")
    
    gene_list = forms.CharField(widget=forms.Textarea, required=False, label="GENE LIST")
    exclude_gene_list = forms.CharField(widget=forms.Textarea, required=False, label="EXCLUDE GENE LIST")
#    genegroups = forms.ChoiceField(required=False, choices=GENE_GROUPS, label="Gene Groups")
    genegroups = forms.ModelChoiceField(queryset=GeneGroup.objects.all(), empty_label="-------------", required=False)
    
    genes_in_common = forms.BooleanField(required=False, label="SHOW ONLY VARIANTS PRESENT IN COMMON GENES BETWEEN ALL THE INDIVIDUALS SELECTED")
    positions_in_common = forms.BooleanField(required=False, label="SHOW ONLY VARIANTS AT EXACTLY SAME POSITION BETWEEN ALL THE INDIVIDUALS SELECTED")
    is_at_hgmd = forms.BooleanField(required=False, label="SHOW ONLY VARIANTS PRESENT AT HGMD")
    exclude_varisnp = forms.BooleanField(required=False, label="EXCLUDE VARIANTS AT VARISNP")
    
    

    #denormalize, should be a simple select or even in python :)
    CHOICES = [(x, x.replace('_', ' ')) for x in ['CDS', 'CHROMOSOME_LARGE DELETION', 'CODON_CHANGE', 'CODON_INSERTION', 'CODON_CHANGE_PLUS CODON_INSERTION', 'CODON_DELETION', 'CODON_CHANGE_PLUS CODON_DELETION', 'DOWNSTREAM', 'EXON', 'EXON_DELETED', 'FRAME_SHIFT', 'GENE', 'INTERGENIC', 'INTERGENIC_CONSERVED', 'INTRAGENIC', 'INTRON', 'INTRON_CONSERVED', 'MICRO_RNA', 'NON_SYNONYMOUS_CODING', 'NON_SYNONYMOUS_START', 'NON_SYNONYMOUS_STOP', 'RARE_AMINO_ACID', 'SPLICE_SITE_ACCEPTOR', 'SPLICE_SITE_DONOR', 'SPLICE_SITE_REGION', 'SPLICE_SITE_BRANCH', 'SPLICE_SITE_BRANCH_U12', 'STOP_LOST', 'START_GAINED', 'START_LOST', 'STOP_GAINED', 'SYNONYMOUS_CODING', 'SYNONYMOUS_START', 'SYNONYMOUS_STOP', 'TRANSCRIPT', 'REGULATION', 'UPSTREAM', 'UTR_3_PRIME', 'UTR_3_DELETED', 'UTR_5_PRIME', 'UTR_5_DELETED']]

    # use SnpeffAnnotation
    # (x[0], x[0].replace('_', ' ')) for x in Variant.objects.values_list('snpeff_effect').distinct().order_by('snpeff_effect')

    effect = forms.MultipleChoiceField(choices=CHOICES, required=False)
    # effect = forms.MultipleChoiceField(choices=[(x[0], x[0]) for x in Variant.objects.values_list('snpeff_effect').distinct().order_by('snpeff_effect')], required=False)
    
    CHOICES = [(x, x.replace('_', ' ')) for x in ['NONE', 'SILENT', 'MISSENSE', 'NONSENSE']]

    #[(x[0], x[0]) for x in Variant.objects.values_list('snpeff_functional_class').distinct().exclude(snpeff_functional_class='').order_by('snpeff_functional_class')]

    func_class = forms.MultipleChoiceField(choices=CHOICES, required=False)
    

    CHOICES = [(x, x.replace('_', ' ')) for x in ['HIGH', 'MODERATE', 'MODIFIER', 'LOW']]

    #[(x[0], x[0]) for x in Variant.objects.values_list('snpeff_impact').distinct().order_by('snpeff_impact')]

    impact = forms.MultipleChoiceField(choices=CHOICES, required=False)

    CHOICES = (
               ('.', '.'),
               ('PASS', 'PASS'),
               )
    filter = forms.MultipleChoiceField(choices=CHOICES, required=False)

    # filter = forms.MultipleChoiceField(choices=[(x[0], x[0]) for x in Variant.objects.values_list('filter').distinct().order_by('filter')], required=False)
    
    dbsnp = forms.BooleanField(required=False, label="EXCLUDE ALL VARIANTS PRESENT IN LATEST DBSNP BUILD")
    
    #100genomes freqeuncy
    CHOICES = (('<', '<= '),
               ('>', '>= '),
               ('=', '='),)
    
    genomes1000 = forms.CharField(max_length=50, required=False, label="1000 GENOMES FREQUENCY")
    genomes1000_exclude = forms.BooleanField(required=False, label="EXCLUDE ALL VARIANTS PRESENT IN 1000GENOMES")
    
    #DBSNP Frequency
#    dbsnp_freq_option = forms.ChoiceField(required=False, choices=CHOICES, label="DBSNP Frequency")
    dbsnp_frequency = forms.CharField(max_length=50, required=False, label="")
    dbsnp_exclude = forms.BooleanField(required=False, label="EXCLUDE ALL VARIANTS PRESENT IN DBSNP")
    
    #Variation Server Frequency
#    variationserver_option = forms.ChoiceField(required=False, choices=CHOICES, label="ESP5400 Frequency")
    esp_frequency = forms.CharField(max_length=50, required=False, label="")
    esp_exclude = forms.BooleanField(required=False, label="EXCLUDE ALL VARIANTS PRESENT IN EXOME SEQUENCING PROJECT")
    
    # hi_frequency = forms.CharField(max_length=50, required=False, label="")
    # hi_exclude = forms.BooleanField(required=False, label="Exclude all variants not in genes with Haploinsufficiency")


    #SIFT
#    ljb_sift_class = forms.ChoiceField(choices=[(x[0], x[0]) for x in Variant.objects.values_list('ljb_sift_pred').distinct().exclude(ljb_sift_pred='').order_by('ljb_sift_pred')], required=False)
    
    sift = forms.CharField(max_length=50, required=False, label="SIFT SCORE")
    sift_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT SIFT SCORE")
    
    #POLYPHEN
    # polyphen_option = forms.ChoiceField(required=False, choices=CHOICES, label="Polyphen2 Option")
    polyphen = forms.CharField(max_length=50, required=False, label="POLYPHEN2 FREQUENCY")
    polyphen_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT POLYPHEN SCORE")

    cadd = forms.CharField(max_length=50, required=False, label="CADD SCORE")
    cadd_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT CADD SCORE")

    mcap = forms.CharField(max_length=50, required=False, label="M-CAP SCORE")
    mcap_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT M-CAP SCORE")

    rf_score = forms.CharField(max_length=50, required=False, label="RF SCORE")
    rf_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT RF SCORE")

    ada_score = forms.CharField(max_length=50, required=False, label="ADA SCORE")
    ada_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT ADA SCORE")
    
    mendelmd_score = forms.CharField(max_length=50, required=False, label="MENDEL,MD SCORE")
    
    dbsnp_option = forms.ChoiceField(required=False, choices=CHOICES, label="DBSNP BUILD")#initial='>',
    dbsnp_build = forms.CharField(max_length=50, required=False, label="DBSNP BUILD")#initial='130'
    
    read_depth_option = forms.ChoiceField(required=False, choices=CHOICES, label="READ DEPTH")
    read_depth = forms.CharField(max_length=50, required=False, label="")
    
    qual_option = forms.ChoiceField(required=False, choices=CHOICES, label="QUAL")
    qual = forms.CharField(max_length=50, required=False, label="")
    
    variants_per_gene_option = forms.ChoiceField(required=False, choices=CHOICES, label="VARIANTS PER GENE")
    variants_per_gene = forms.CharField(max_length=50, required=False, label="")
    
    #diseases
    # diseases = forms.MultipleChoiceField(choices=[(x[0], x[0]) for x in Disease.objects.values_list('name').distinct()], required=False)
    
    fields = forms.MultipleChoiceField(choices=FIELDS, required=False)
    
    # conditions = forms.ModelMultipleChoiceField(queryset=CGDCondition.objects.filter().order_by('name'), required=False)
    
    # omim = forms.ModelMultipleChoiceField(queryset=Disease.objects.filter().order_by('name'), required=False)
    
    # omim = MultiOmimChoices()

    omim = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        queryset=Disease.objects.all(),
        search_fields=['name__icontains'],
    ), queryset=Disease.objects.all(), required=True)

    cgd = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        queryset=CGDCondition.objects.all(),
        search_fields=['name__icontains'],
    ), queryset=CGDCondition.objects.all(), required=True)
    # hgmd = MultiHgmdChoices()

    cgdmanifestation = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        queryset=Manifestation.objects.all(),
        search_fields=['name__icontains'],
    ), queryset=Manifestation.objects.all(), required=True)
    
    # hgmd = forms.ModelMultipleChoiceField(queryset=HGMDPhenotype.objects.filter().order_by('name'), required=False)

    genelists = forms.ModelMultipleChoiceField(queryset=GeneList.objects.all().order_by('name'), required=False, label="SAVED GENE LIST")
    exclude_genelists = forms.ModelMultipleChoiceField(queryset=GeneList.objects.all().order_by('name'), required=False, label="EXCLUDE SAVED GENE LIST")

    def __init__(self, user=None, *args, **kwargs):

        super(FilterAnalysisForm, self).__init__(*args, **kwargs)

        if not user.is_authenticated:
            # print('user None', user)
            self.fields['individuals'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=None).order_by('id'), required=False, label='INDIVIDUALS')
            self.fields['exclude_individuals'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=None).order_by('id'), required=False, label='INDIVIDUALS')
        else:
            print('user', user)
            if user.is_superuser:
                self.fields['individuals'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter().order_by('id'), required=False, label='INDIVIDUALS')
                self.fields['exclude_individuals'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter().order_by('id'), required=False, label='INDIVIDUALS')
            else:
                self.fields['individuals'] = forms.ModelMultipleChoiceField(
                    queryset=Individual.objects.filter(Q(user=user) | Q(user=None)).order_by('id'), required=False, label='INDIVIDUALS')
                self.fields['exclude_individuals'] = forms.ModelMultipleChoiceField(
                    queryset=Individual.objects.filter(Q(user=user) | Q(user=None)).order_by('id'), required=False, label='INDIVIDUALS')
        # self.fields['sift'].widget.attrs['readonly'] = True
        # self.fields['polyphen'].widget.attrs['readonly'] = True
        # self.fields['genomes1000'].widget.attrs['readonly'] = True
        # self.fields['dbsnp_frequency'].widget.attrs['readonly'] = True
        # self.fields['esp_frequency'].widget.attrs['readonly'] = True
         

#trio analysis
class FamilyAnalysisForm(forms.Form):

    chr = forms.CharField(max_length=50, required=False, label='CHR')
    pos = forms.CharField(max_length=50, required=False, label='POS')
    
    snp_list = forms.CharField(widget=forms.Textarea, required=False, label='SNP LIST')
    exclude_snp_list = forms.CharField(widget=forms.Textarea, required=False, label='EXCLUDE SNP LIST')
    
    #individuals = forms.MultipleChoiceField(choices=[(x.id, x.name) for x in Individual.objects.filter().order_by('id')], required=False)
    individuals = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False, label='INDIVIDUALS')
    exclude_individuals = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False, label='EXCLUDE INDIVIDUALS')

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all().order_by('id'), required=False, label='GROUPS')
    exclude_groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all().order_by('id'), required=False, label='EXCLUDE GROUPS')

    
    # CHOICES = (('', ''),
    #            ('recessive', 'recessive'),
    #            ('dominant', 'dominant'),
    #            )
    # inheritance_model = forms.ChoiceField(required=False, choices=CHOICES, label="Inheritance Model")
    CHOICES = (('', ''),
               ('homozygous', 'HOMOZYGOUS  (Ex. 1/1, 2/1, 1/2)'),
               ('heterozygous', 'HETEROZYGOUS  (Ex. 0/1, 0/2, 1/0, 2/0)'),
               )
    mutation_type = forms.ChoiceField(required=False, choices=CHOICES, label="MUTATION TYPE")
    
    gene_list = forms.CharField(widget=forms.Textarea, required=False, label="GENE LIST")
    exclude_gene_list = forms.CharField(widget=forms.Textarea, required=False, label="EXCLUDE GENE LIST")
#    genegroups = forms.ChoiceField(required=False, choices=GENE_GROUPS, label="Gene Groups")
    genegroups = forms.ModelChoiceField(queryset=GeneGroup.objects.all(), empty_label="-------------", required=False)
    
    genes_in_common = forms.BooleanField(required=False, label="SHOW ONLY VARIANTS PRESENT IN COMMON GENES BETWEEN ALL THE INDIVIDUALS SELECTED")
    positions_in_common = forms.BooleanField(required=False, label="SHOW ONLY VARIANTS AT EXACTLY SAME POSITION BETWEEN ALL THE INDIVIDUALS SELECTED")
    is_at_hgmd = forms.BooleanField(required=False, label="SHOW ONLY VARIANTS PRESENT AT HGMD")
    exclude_varisnp = forms.BooleanField(required=False, label="EXCLUDE VARIANTS AT VARISNP")
    
    

    #denormalize, should be a simple select or even in python :)
    # CHOICES = [(x, x.replace('_', ' ')) for x in ['CDS', 'CHROMOSOME_LARGE DELETION', 'CODON_CHANGE', 'CODON_INSERTION', 'CODON_CHANGE_PLUS CODON_INSERTION', 'CODON_DELETION', 'CODON_CHANGE_PLUS CODON_DELETION', 'DOWNSTREAM', 'EXON', 'EXON_DELETED', 'FRAME_SHIFT', 'GENE', 'INTERGENIC', 'INTERGENIC_CONSERVED', 'INTRAGENIC', 'INTRON', 'INTRON_CONSERVED', 'MICRO_RNA', 'NON_SYNONYMOUS_CODING', 'NON_SYNONYMOUS_START', 'NON_SYNONYMOUS_STOP', 'RARE_AMINO_ACID', 'SPLICE_SITE_ACCEPTOR', 'SPLICE_SITE_DONOR', 'SPLICE_SITE_REGION', 'SPLICE_SITE_BRANCH', 'SPLICE_SITE_BRANCH_U12', 'STOP_LOST', 'START_GAINED', 'START_LOST', 'STOP_GAINED', 'SYNONYMOUS_CODING', 'SYNONYMOUS_START', 'SYNONYMOUS_STOP', 'TRANSCRIPT', 'REGULATION', 'UPSTREAM', 'UTR_3_PRIME', 'UTR_3_DELETED', 'UTR_5_PRIME', 'UTR_5_DELETED']]

    # use SnpeffAnnotation
    # (x[0], x[0].replace('_', ' ')) for x in Variant.objects.values_list('snpeff_effect').distinct().order_by('snpeff_effect')

    # effect = forms.MultipleChoiceField(choices=CHOICES, required=False)
    # effect = forms.MultipleChoiceField(choices=[(x[0], x[0]) for x in Variant.objects.values_list('snpeff_effect').distinct().order_by('snpeff_effect')], required=False)
    CHOICES = [(x, x.replace('_', ' ')) for x in ['CDS', 'CHROMOSOME_LARGE DELETION', 'CODON_CHANGE', 'CODON_INSERTION', 'CODON_CHANGE_PLUS CODON_INSERTION', 'CODON_DELETION', 'CODON_CHANGE_PLUS CODON_DELETION', 'DOWNSTREAM', 'EXON', 'EXON_DELETED', 'FRAME_SHIFT', 'GENE', 'INTERGENIC', 'INTERGENIC_CONSERVED', 'INTRAGENIC', 'INTRON', 'INTRON_CONSERVED', 'MICRO_RNA', 'NON_SYNONYMOUS_CODING', 'NON_SYNONYMOUS_START', 'NON_SYNONYMOUS_STOP', 'RARE_AMINO_ACID', 'SPLICE_SITE_ACCEPTOR', 'SPLICE_SITE_DONOR', 'SPLICE_SITE_REGION', 'SPLICE_SITE_BRANCH', 'SPLICE_SITE_BRANCH_U12', 'STOP_LOST', 'START_GAINED', 'START_LOST', 'STOP_GAINED', 'SYNONYMOUS_CODING', 'SYNONYMOUS_START', 'SYNONYMOUS_STOP', 'TRANSCRIPT', 'REGULATION', 'UPSTREAM', 'UTR_3_PRIME', 'UTR_3_DELETED', 'UTR_5_PRIME', 'UTR_5_DELETED']]

    effect = forms.MultipleChoiceField(choices=CHOICES, required=False)

    CHOICES = [(x, x.replace('_', ' ')) for x in ['NONE', 'SILENT', 'MISSENSE', 'NONSENSE']]

    func_class = forms.MultipleChoiceField(choices=CHOICES, required=False)
    

    CHOICES = [(x, x.replace('_', ' ')) for x in ['HIGH', 'MODERATE', 'MODIFIER', 'LOW']]

    #[(x[0], x[0]) for x in Variant.objects.values_list('snpeff_impact').distinct().order_by('snpeff_impact')]

    impact = forms.MultipleChoiceField(choices=CHOICES, required=False)
    
    # filter = forms.MultipleChoiceField(choices=[(x[0], x[0]) for x in Variant.objects.values_list('filter').distinct().order_by('filter')], required=False)
    CHOICES = (
               ('.', '.'),
               ('PASS', 'PASS'),
               )
    filter = forms.MultipleChoiceField(choices=CHOICES, required=False)

    dbsnp = forms.BooleanField(required=False, label="EXCLUDE ALL VARIANTS PRESENT IN LATEST DBSNP BUILD")
    
    #100genomes freqeuncy
    CHOICES = (('<', '<= '),
               ('>', '>= '),
               ('=', '='),)
    
    genomes1000 = forms.CharField(max_length=50, required=False, label="1000 GENOMES FREQUENCY")
    genomes1000_exclude = forms.BooleanField(required=False, label="EXCLUDE ALL VARIANTS PRESENT IN 1000GENOMES")
    
    #DBSNP Frequency
#    dbsnp_freq_option = forms.ChoiceField(required=False, choices=CHOICES, label="DBSNP Frequency")
    dbsnp_frequency = forms.CharField(max_length=50, required=False, label="")
    dbsnp_exclude = forms.BooleanField(required=False, label="EXCLUDE ALL VARIANTS PRESENT IN DBSNP")
    
    #Variation Server Frequency
#    variationserver_option = forms.ChoiceField(required=False, choices=CHOICES, label="ESP5400 Frequency")
    esp_frequency = forms.CharField(max_length=50, required=False, label="")
    esp_exclude = forms.BooleanField(required=False, label="EXCLUDE ALL VARIANTS PRESENT IN EXOME SEQUENCING PROJECT")
    
    # hi_frequency = forms.CharField(max_length=50, required=False, label="")
    # hi_exclude = forms.BooleanField(required=False, label="Exclude all variants not in genes with Haploinsufficiency")


    #SIFT
#    ljb_sift_class = forms.ChoiceField(choices=[(x[0], x[0]) for x in Variant.objects.values_list('ljb_sift_pred').distinct().exclude(ljb_sift_pred='').order_by('ljb_sift_pred')], required=False)
    
    sift = forms.CharField(max_length=50, required=False, label="SIFT SCORE")
    sift_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT SIFT SCORE")
    
    #POLYPHEN
    # polyphen_option = forms.ChoiceField(required=False, choices=CHOICES, label="Polyphen2 Option")
    polyphen = forms.CharField(max_length=50, required=False, label="POLYPHEN2 FREQUENCY")
    polyphen_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT POLYPHEN SCORE")

    cadd = forms.CharField(max_length=50, required=False, label="CADD SCORE")
    cadd_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT CADD SCORE")

    rf_score = forms.CharField(max_length=50, required=False, label="RF SCORE")
    rf_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT RF SCORE")

    ada_score = forms.CharField(max_length=50, required=False, label="ADA SCORE")
    ada_exclude = forms.BooleanField(required=False, label="EXCLUDE VARIANTS WITHOUT ADA SCORE")
    
    mendelmd_score = forms.CharField(max_length=50, required=False, label="MENDEL,MD SCORE")
    
    dbsnp_option = forms.ChoiceField(required=False, choices=CHOICES, label="DBSNP BUILD")#initial='>',
    dbsnp_build = forms.CharField(max_length=50, required=False, label="DBSNP BUILD")#initial='130'
    
    read_depth_option = forms.ChoiceField(required=False, choices=CHOICES, label="READ DEPTH")
    read_depth = forms.CharField(max_length=50, required=False, label="")
    
    qual_option = forms.ChoiceField(required=False, choices=CHOICES, label="QUAL")
    qual = forms.CharField(max_length=50, required=False, label="")
    
    variants_per_gene_option = forms.ChoiceField(required=False, choices=CHOICES, label="VARIANTS PER GENE")
    variants_per_gene = forms.CharField(max_length=50, required=False, label="")
    
    #diseases
    # diseases = forms.MultipleChoiceField(choices=[(x[0], x[0]) for x in Disease.objects.values_list('name').distinct()], required=False)
    
    fields = forms.MultipleChoiceField(choices=FIELDS, required=False)
    
    omim = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        queryset=Disease.objects.all(),
        search_fields=['name__icontains'],
    ), queryset=Disease.objects.all(), required=True)

    cgd = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        queryset=CGDCondition.objects.all(),
        search_fields=['name__icontains'],
    ), queryset=CGDCondition.objects.all(), required=True)
    # hgmd = MultiHgmdChoices()

    cgdmanifestation = forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(
        queryset=Manifestation.objects.all(),
        search_fields=['name__icontains'],
    ), queryset=Manifestation.objects.all(), required=True)
    
    
    # hgmd = forms.ModelMultipleChoiceField(queryset=HGMDPhenotype.objects.filter().order_by('name'), required=False)

    genelists = forms.ModelMultipleChoiceField(queryset=GeneList.objects.all().order_by('name'), required=False, label="SAVED GENE LIST")
    exclude_genelists = forms.ModelMultipleChoiceField(queryset=GeneList.objects.all().order_by('name'), required=False, label="EXCLUDE SAVED GENE LIST")
    
    mother = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False)
    father = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False)
    children = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False)
    INHERITANCE_CHOICES = (('', ''),
               ('recessive', 'Autosomal Recessive'),
               ('dominant', 'Autosomal Dominant'),
               ('compound heterozygous', 'Autosomal Compound Heterozygous'),
               ('xlinked recessive', 'X-linked Recessive'),
               ('xlinked dominant', 'X-linked Dominant'),               # ('recessive denovo', 'Autsomal Recessive denovo'),
               # ('dominant denovo', 'Autsomal Dominant denovo'),
               # ('xlinked dominant denovo', 'X-linked dominant de novo'),
               # ('xlinked recessive denovo', 'X-linked Recessive de novo'),

               )
    inheritance_option = forms.ChoiceField(choices=INHERITANCE_CHOICES, required=False)
    
    def __init__(self, user=None, *args, **kwargs):
        
        super(FamilyAnalysisForm, self).__init__(*args, **kwargs)

        if not user.is_authenticated:
            # print('user None', user)
            self.fields['mother'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=None).order_by('id'), required=False)
            self.fields['father'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=None).order_by('id'), required=False)
            self.fields['children'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=None).order_by('id'), required=False)
            self.fields['exclude_individuals'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=None).order_by('id'), required=False)
        else:
            # print('user', user)
            self.fields['mother'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=user).order_by('id'), required=False)
            self.fields['father'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=user).order_by('id'), required=False)
            self.fields['children'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=user).order_by('id'), required=False)
            self.fields['exclude_individuals'] = forms.ModelMultipleChoiceField(queryset=Individual.objects.filter(user=user).order_by('id'), required=False)


# INDIVIDUALS = [(x.id, x.name) for x in Individual.objects.all().order_by('id')]
INDIVIDUALS = []

#forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'))
class FilterWiZardForm1(forms.Form):
    individuals = forms.ModelMultipleChoiceField(queryset=Individual.objects.all().order_by('id'), required=False)#choices=INDIVIDUALS, 
    exclude_individuals = forms.MultipleChoiceField(choices=INDIVIDUALS, required=False)
    
    # groups = forms.MultipleChoiceField(choices=[(x.id, x.name) for x in Group.objects.all().order_by('id')], required=False)
    
    # exclude_groups = forms.MultipleChoiceField(choices=[(x.id, x.name) for x in Group.objects.all().order_by('id')], required=False)
    
    snp_list = forms.CharField(widget=forms.Textarea, required=False)
    exclude_snp_list = forms.CharField(widget=forms.Textarea, required=False)
    
    
    gene_list = forms.CharField(widget=forms.Textarea, required=False)
    exclude_gene_list = forms.CharField(widget=forms.Textarea, required=False)
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        INDIVIDUALS = [(x.id, x.name) for x in Individual.objects.all().order_by('id')]

    
class FilterWiZardForm2(forms.Form):
    #variant type
    CHOICES = (('', ''),
               ('homozygous', 'Homozygous  (Ex. 1/1, 2/1, 1/2)'),
               ('heterozygous', 'Heterozygous  (Ex. 0/1, 0/2, 1/0, 2/0)'),
               )
    mutation_type = forms.ChoiceField(required=False, choices=CHOICES, label="Mutation Type", initial="homozygous")

    #About Variant
    chr = forms.CharField(max_length=50, required=False)
    pos = forms.CharField(max_length=50, required=False)
    
    genegroups = forms.ModelChoiceField(queryset=GeneGroup.objects.all(), empty_label="-------------", required=False)
    
    
    CHOICES = ['CDS', 'CHROMOSOME_LARGE DELETION', 'CODON_CHANGE', 'CODON_INSERTION', 'CODON_CHANGE_PLUS CODON_INSERTION', 'CODON_DELETION', 'CODON_CHANGE_PLUS CODON_DELETION', 'DOWNSTREAM', 'EXON', 'EXON_DELETED', 'FRAME_SHIFT', 'GENE', 'INTERGENIC', 'INTERGENIC_CONSERVED', 'INTRAGENIC', 'INTRON', 'INTRON_CONSERVED', 'MICRO_RNA', 'NON_SYNONYMOUS_CODING', 'NON_SYNONYMOUS_START', 'NON_SYNONYMOUS_STOP', 'RARE_AMINO_ACID', 'SPLICE_SITE_ACCEPTOR', 'SPLICE_SITE_DONOR', 'SPLICE_SITE_REGION', 'SPLICE_SITE_BRANCH', 'SPLICE_SITE_BRANCH_U12', 'STOP_LOST', 'START_GAINED', 'START_LOST', 'STOP_GAINED', 'SYNONYMOUS_CODING', 'SYNONYMOUS_START', 'SYNONYMOUS_STOP', 'TRANSCRIPT', 'REGULATION', 'UPSTREAM', 'UTR_3_PRIME', 'UTR_3_DELETED', 'UTR_5_PRIME', 'UTR_5_DELETED']

    # use SnpeffAnnotation
    # (x[0], x[0].replace('_', ' ')) for x in Variant.objects.values_list('snpeff_effect').distinct().order_by('snpeff_effect')

    effect = forms.MultipleChoiceField(choices=CHOICES, required=False)
    
    CHOICES = ['NONE', 'SILENT', 'MISSENSE', 'NONSENSE']
     
    #[(x[0], x[0]) for x in Variant.objects.values_list('snpeff_functional_class').distinct().exclude(snpeff_functional_class='').order_by('snpeff_functional_class')]
    func_class = forms.MultipleChoiceField(choices=CHOICES, required=False)
    

    CHOICES = ['HIGH', 'MODERATE', 'MODIFIER', 'LOW']

    #[(x[0], x[0]) for x in Variant.objects.values_list('snpeff_impact').distinct().order_by('snpeff_impact')]

    impact = forms.MultipleChoiceField(choices=CHOICES, required=False)
    
    CHOICES = (('<', '<= '),
               ('>', '>= '),
               ('=', '='),)
    
    dbsnp_option = forms.ChoiceField(required=False, choices=CHOICES, label="dbSNP Build")
    dbsnp_build = forms.CharField(max_length=50, required=False, label="DbsNP Build")
    
    read_depth_option = forms.ChoiceField(required=False, choices=CHOICES, label="Read Depth", initial='>')
    read_depth = forms.CharField(max_length=50, required=False, label="", initial='10')
    
    variants_per_gene_option = forms.ChoiceField(required=False, choices=CHOICES, label="Variants per Gene")
    variants_per_gene = forms.CharField(max_length=50, required=False, label="")
    
    #Extra options
    genes_in_common = forms.BooleanField(required=False, label="Show only variants present in genes from all the individuals selected", initial=True)
    dbsnp = forms.BooleanField(required=False, label="Show only variants with rsID in dbSNP")
    cln = forms.BooleanField(required=False, label="Show only variants with clinical association")
    exclude_segdup = forms.BooleanField(required=False, label="Exclude variants in regions of Segmental Duplications", initial=True)
    

class FilterWiZardForm3(forms.Form):
    #100genomes freqeuncy
    CHOICES = (('<', '<= '),
               ('>', '>= '),
               ('=', '='),)
    #1000Genomes
    # genomes1000_option = forms.ChoiceField(required=False, choices=CHOICES, label="1000genomes Frequency")
    genomes1000 = forms.CharField(max_length=50, required=False, label="1000genomes Frequency", initial="0 - 0.005")
    genomes1000_exclude = forms.BooleanField(required=False, label="Exclude all variants present in 1000genomes")
    #DBSNP Frequency
    # dbsnp_freq_option = forms.ChoiceField(required=False, choices=CHOICES, label="DBSNP Frequency")
    dbsnp_frequency = forms.CharField(max_length=50, required=False, label="", initial="0 - 0.005")
    dbsnp_exclude = forms.BooleanField(required=False, label="Exclude all variants present in dbSNP")
    
    #Variation Server Frequency
    # variationserver_option = forms.ChoiceField(required=False, choices=CHOICES, label="ESP5400 Frequency")
    esp_frequency = forms.CharField(max_length=50, required=False, label="", initial="0 - 0.005")
    esp_exclude = forms.BooleanField(required=False, label="Exclude all variants present in Exome Sequencing Project")
    
    # sift_option = forms.ChoiceField(required=False, choices=CHOICES, label="Sift Option")
    sift = forms.CharField(max_length=50, required=False, label="Sift Frequency", initial="0 - 1.0")
    sift_exclude = forms.BooleanField(required=False, label="Exclude variants without sift score", initial=False)
    
    #POLYPHEN
    # polyphen_option = forms.ChoiceField(required=False, choices=CHOICES, label="Polyphen2 Option", initial='>')
    polyphen = forms.CharField(max_length=50, required=False, label="Polyphen2 Frequency", initial='0 - 1.0')
    polyphen_exclude = forms.BooleanField(required=False, label="Exclude variants without polyphen score", initial=False)
    
    mendelmd_score = forms.CharField(max_length=50, required=False, label="Mendel,MD Score", initial='3 - 12')
    
    
