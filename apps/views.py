from django.shortcuts import render
from .models import WebApp

from servers.models import Server

def index(request):
    webapp_list = WebApp.objects.all()  # .order_by("-pub_date")[:5]
    context = {"webapp_list": webapp_list}
    return render(request, "apps/index.html", context)

def import_apps(request):
	print('import apps')


	servers=Server.objects.all()
	for server in servers:
		print(server.name,server.ip)
		

	webapp_list = WebApp.objects.all()  # .order_by("-pub_date")[:5]
	context = {"webapp_list": webapp_list}

	return render(request, "apps/index.html", context)
