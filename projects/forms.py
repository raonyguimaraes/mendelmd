from django.db import models
from django.forms import ModelForm
from .models import Project
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'groups', 'members']
        # fields = '__all__'

class ImportFilesForm(forms.Form):
    file_list = forms.CharField(widget=forms.Textarea)