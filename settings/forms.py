from django.db import models
from django.forms import ModelForm
from .models import S3Credential

class S3CredentialForm(ModelForm):
    class Meta:
        model = S3Credential
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(S3CredentialForm, self).__init__(*args, **kwargs)
