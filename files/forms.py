from django.forms import ModelForm
from django import forms
from .models import File

class UploadForm(ModelForm):

    vcf_file = forms.CharField(max_length=600, required=False)

    class Meta:
        model = File
        fields = '__all__'

# class FileForm(forms.Form):
#     OPTIONS = (
#                 ("fastq", "fastq"),
#                 ("bam", "bam"),
#                 ("vcf", "vcf"),
#                 )
    # extension = forms.MultipleChoiceField(choices=OPTIONS, required=False)
