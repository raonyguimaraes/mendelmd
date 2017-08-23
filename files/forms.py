from django.db import models
from django.forms import ModelForm
from .models import S3Credential

class S3CredentialForm(ModelForm):
    class Meta:
        model = S3Credential
        fields = '__all__'
