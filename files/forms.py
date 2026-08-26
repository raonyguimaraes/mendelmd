from django.forms import ModelForm
from .models import File

class UploadForm(ModelForm):

    class Meta:
        model = File
        fields = ['name']

# class FileForm(forms.Form):
#     OPTIONS = (
#                 ("fastq", "fastq"),
#                 ("bam", "bam"),
#                 ("vcf", "vcf"),
#                 )
    # extension = forms.MultipleChoiceField(choices=OPTIONS, required=False)
