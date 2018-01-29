from django import forms

class ContactForm1(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()

class ContactForm2(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class CreateAnalysis(forms.Form):
    name = forms.CharField(max_length=100)
    project = forms.CharField(widget=forms.Textarea)
    settings = forms.CharField(widget=forms.Textarea)
