from django.forms import ModelForm
from cases.models import Case
from django import forms
from individuals.models import Individual

# Create the form class.
class CaseForm(ModelForm):
    class Meta:
        model = Case
        fields = '__all__'