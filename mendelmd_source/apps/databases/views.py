# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

@login_required
def index(request):

    return render(request, 'databases/index.html')
