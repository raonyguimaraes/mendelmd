from django import forms

class ContactForm1(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()

class ContactForm2(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

ANALYSIS_TYPES = (
    ('alignment', 'alignment'),    
    ('variant calling', 'variant calling'),
    ('cnv identification', 'cnv identification'),
)

class CreateAnalysis(forms.Form):
    name = forms.CharField(max_length=100)
    project = forms.CharField(widget=forms.Textarea)
    settings = forms.CharField(widget=forms.Textarea)
    analysis_types = forms.MultipleChoiceField(
        required=False,
        choices=ANALYSIS_TYPES,
    )

