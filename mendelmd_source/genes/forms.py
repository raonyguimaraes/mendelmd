from django import forms
from genes.models import GeneGroup
from django.forms import ModelForm

class GeneGroupForm(ModelForm):
    class Meta:
        model = GeneGroup
        fields = '__all__'


class GenesetForm(forms.Form):
  name = forms.CharField(max_length=255)
  genes = forms.CharField(widget=forms.widgets.Textarea())

  def __init__(self, *args, **kwargs):
      self.instance = kwargs.pop('instance', None)
      super(GenesetForm, self).__init__(*args, **kwargs)
      # self.fields['tags'].choices = [(tag.id, tag.title) for tag in Tag.objects]
      if self.instance:
          self.fields['name'].initial = self.instance.name
          self.fields['genes'].initial = self.instance.genes
          # self.fields['is_published'].initial = self.instance.is_published        
          # self.fields['tags'].initial = [tag.id for tag in self.instance.tags]


  