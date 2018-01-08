from django.db import models
from django.forms import ModelForm
from .models import Project
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'paths', 'groups', 'members']
        # fields = '__all__'

class ImportForm(forms.Form):
    path = forms.CharField(required=False)
    file_list = forms.CharField(widget=forms.Textarea, required=False)
    samples = forms.CharField(widget=forms.Textarea, required=False)