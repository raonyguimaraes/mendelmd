from django import forms

class SampleGroupForm(forms.Form):
    name = forms.CharField(max_length=100)
