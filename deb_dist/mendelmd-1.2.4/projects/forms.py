from django.db import models
from django.forms import ModelForm
from .models import Project
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'groups']#, 'members', #'paths', 
        # fields = '__all__'

class ImportForm(forms.Form):
    # paths = forms.CharField(widget=forms.Textarea, required=False)
    file_list = forms.CharField(widget=forms.Textarea, required=False)
    samples = forms.CharField(widget=forms.Textarea, required=False)