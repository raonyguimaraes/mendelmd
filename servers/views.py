from django.shortcuts import render
# hvloud reqs
from hcloud import Client

from keys.models import CloudKey
from .models import Server

client = Client(token="{YOUR_API_TOKEN}")  # Please paste your API token here


def index(request):
    server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    context = {"server_list": server_list}
    return render(request, "servers/index.html", context)


def import_from_hetzner(request):
    print('Import Servers!')
    hetznerkey = CloudKey.objects.get(cloudprovider="Hetzner")
    print(hetznerkey.key)

    client = Client(token=hetznerkey.key)  # Please paste your API token here
    # List your servers
    servers = client.servers.get_all()

    Server.objects.all().delete()

    for server in servers:
        print(f"{server.id=} {server.name=} {server.status=}")
        # print(server.public_net.ipv4_address)
        # print(server.public_net)
        # print(server.public_net.ipv4)
        print(server.public_net.ipv4.ip)
        server_object = Server(
            name=server.name,
            ip=server.public_net.ipv4.ip)
        server_object.save()

    server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    context = {"server_list": server_list}
    return render(request, "servers/index.html", context)
