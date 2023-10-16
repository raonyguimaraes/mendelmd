from django import forms
from .models import Server


# creating a form
class ServerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,required=False)
    class Meta:
        # specify model to be used
        model = Server
        fields = '__all__'
        #
        # # specify fields to be used
        # fields = [
        #     "title",
        #     "description",
        # ]
