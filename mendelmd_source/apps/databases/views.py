# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

@login_required
def index(request):

    return render_to_response('databases/index.html', context_instance=RequestContext(request))
