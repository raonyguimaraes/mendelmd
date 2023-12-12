from django.shortcuts import render
from django.shortcuts import redirect
from individuals.models import Individual
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    if request.method == 'POST':
        status = request.POST['status']
        # print('status', status)
    else:
        status = ''
    if request.user.is_staff:
        if status != '':
            individuals = Individual.objects.filter(status=status).order_by('-id')
        else:
            individuals = Individual.objects.all().order_by('-id')
    elif request.user.is_authenticated:
        individuals = Individual.objects.filter(user=request.user).order_by('-id')
    else:
        individuals = Individual.objects.filter(user=None).order_by('-id')

    n_individuals = individuals.count()

    paginator = Paginator(individuals, 1000) # Show 25 contacts per page

    page = request.GET.get('page')

    try:
        individuals = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        individuals = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        individuals = paginator.page(paginator.num_pages)


    context = {
    'n_individuals': n_individuals,
    'individuals':individuals
    }
    return render(request, 'dashboard/dashboard.html', context)


def docs(request):
    return redirect("https://rockbio.readthedocs.io/")