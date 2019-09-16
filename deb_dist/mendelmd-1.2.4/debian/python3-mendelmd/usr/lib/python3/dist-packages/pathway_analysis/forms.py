from django import forms

from filter_analysis.forms import FilterAnalysisForm

class PathAnalysisForm(forms.Form):
    search = forms.CharField(max_length=50, required=False)
    
class PathwayAnalysisForm(FilterAnalysisForm):
    CHOICES = (('<', '<= '),
               ('>', '>= '),
               ('=', '='),)
    individuals_per_pathway_option = forms.ChoiceField(required=False, choices=CHOICES, label="Individuals per Pathway")
    individuals_per_pathway = forms.CharField(max_length=50, required=False, label="") 