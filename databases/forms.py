from django import forms
from .models import Genome1kSample

class Genomes1kForm(forms.Form):
    sample = forms.ModelChoiceField(
        queryset=Genome1kSample.objects.all().order_by('name'),
    )

