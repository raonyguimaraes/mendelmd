from django.shortcuts import render
from django.shortcuts import redirect
from ecommerce_app.models import Product


def index(request):
	# print "Hello"
	#if user is logged redirect
    if request.user.is_authenticated:
        return redirect('dashboard')

    plans = Product.objects.filter(is_subscription=True).order_by('price')
    return render(request, 'pages/index.html', {'plans': plans})

def new_index(request):
	return render(request, 'pages/new_index.html')

def docs(request):
    return redirect("https://mendelmd.readthedocs.io/")
