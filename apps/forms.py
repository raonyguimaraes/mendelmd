from django import forms
from .models import WebApp
from servers.models import Server

# creating a form
class MoveAppForm(forms.ModelForm):
    # destination=forms.CharField(required=True)

    # server_destination = forms.CharField(required=True)
    server_destination = forms.ModelChoiceField(queryset=Server.objects.all())
    INSTALL_TYPES = (
        ('', '-----------'),
        ('local', 'local'),
        ('lxd', 'lxd'),
        ('docker', 'docker'),
    )
    install_type = forms.CharField(widget=forms.Select(choices=INSTALL_TYPES))
    new_dns=forms.CharField(required=True,label='New DNS')
    class Meta:
        # specify model to be used
        model = WebApp
        fields = '__all__'
        #
        # # specify fields to be used
        # fields = [
        #     "title",
        #     "description",
        # ]
