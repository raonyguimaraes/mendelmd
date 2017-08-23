from django.db import models
from django.forms import ModelForm
from .models import Project
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = ['user', 'individuals', 'files', 'name', 'description', 'is_public', 'status', 'members', 'creation_date', 'modified_date']
        fields = '__all__'
