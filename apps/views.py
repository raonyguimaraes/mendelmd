from django.shortcuts import render, redirect, get_object_or_404

from .forms import MoveAppForm
from .models import WebApp
from tasks.models import Task
from subprocess import run,check_output

from servers.models import Server
import paramiko
import json

# class TransferApp:
#     def __init__(self, data):
#         self.data = data  # instance variable unique to each instance
#
#     def transfer(self):
#         print('Here we go!')
#
#         data=self.data
#         print(data)
#
#         #{'name': 'nftower', 'app_folder': '/root/nf-tower', 'server_name': 'nftower',
#         # 'server_ip': '128.140.103.187', 'server_destination': '65.21.255.94', 'install_type': 'local'}
#         #get destination ip
#         #copy files to destination
#         print('copy files to destination:')
#         #bad code that works very slow
#         # command = 'scp -3r -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@{}:{}/ root@{}:{}/'.format(data['server_ip'],data['app_folder'],data['server_destination'],data['app_folder'])
#
#         # command = 'rsync -avz root@{}:{}/ nftower/'.format(data['server_ip'], data['app_folder'])
#         #
#         # # command = 'rsync -avz root@{}:{}/ root@{}:{}/'.format(
#         # # data['server_ip'], data['app_folder'], data['server_destination'], data['app_folder'])
#         # print(command)
#
#         # output = check_output(command, shell=True)
#         # print(output.decode())
#
#     # print(data)

def index(request):
    webapp_list = WebApp.objects.all()  # .order_by("-pub_date")[:5]
    n_apps=webapp_list.count()
    context = {"webapp_list": webapp_list, 'n_apps':n_apps}
    return render(request, "apps/index.html", context)

def detail_view(request, id):
    app=WebApp.objects.get(id=id)
    context = {"app": app}
    return render(request, "apps/detail_view.html", context)
#
# def move_app(request,id):
# 	# add the dictionary during initialization
# 	context = {}
# 	form = MoveAppForm(request.POST or None)
# 	if form.is_valid():
# 		# form.save()
# 		print(form.cleaned_data)
#
# 		#return redirect('webapps_index')
#
# 	context['form'] = form
# 	return render(request, "apps/move_app.html", context)
#

def move_app(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(WebApp, id=id)

    # pass the object as instance in form
    form = MoveAppForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        # form.save()
        print(form.cleaned_data)
        data=form.cleaned_data['data']
        data['server_destination']=form.cleaned_data['server_destination'].ip
        data['install_type'] = form.cleaned_data['install_type']
        data['new_dns'] = form.cleaned_data['new_dns']
        
        data['task_type'] = 'transfer_nf-tower_lxd'

        task=Task(
            name='transfer_app',
            manifest=data
        )
        task.save()
        print('task.id',task.id)
        return redirect('tasks-view',pk=task.id)
        # TransferApp(data).transfer()
        #redirect to task view

        #move app
        #create task

        # return redirect('webapps_index')

    # add form dictionary to context
    context["form"] = form

    return render(request, "apps/move_app.html", context)

def connect_and_find_apps(server):

    ip=server.ip
    username=server.username

    command = 'scp -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null scripts/find_apps.py {}@{}:~/'.format(
        server.username,ip)
    output = check_output(command, shell=True)
    print(output.decode())


    paramikoclient = paramiko.SSHClient()
    paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramikoclient.connect(ip, username=server.username)

    # ssh_stdin, ssh_stdout, ssh_stderr = paramikoclient.exec_command("python3 find_apps.py")
    # exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
    # out=ssh_stdout.read().decode().splitlines()
    # print(out)#.replace('\n', ' '))

    command = 'ssh -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{} python3 find_apps.py'.format(
        username,ip)
    output = check_output(command, shell=True)
    print(output.decode())

    # json_out=ssh_stdout.read().decode().splitlines()
    # print('json_out',json_out)

    sftp_client = paramikoclient.open_sftp()
    file = sftp_client.open('apps.json').read()
    json_object = json.loads(file)

    # if len(json_out)>=1:
    # 	json_out=json_out[-1].strip()
    # 	# print(json_out)
    # 	json_acceptable_string = json_out.replace("'", "\"")
    # 	json_object = json.loads(json_acceptable_string)
    # else:
    # 	json_object={}

    # json_object = {}
    return(json_object)
    #
    # for line in ssh_stdout:
    # 	print(line.strip())
    # command = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@{} python3 find_apps.py'.format(
    # 	ip)
    # output = check_output(command, shell=True)
    # print(output.decode())

def import_apps(request):
    print('import apps')


    servers=Server.objects.all()
    for server in servers:
        print('server', server.name,server.ip)
        #connect and find apps
        apps=connect_and_find_apps(server)
        print('apps',apps)
        if len(apps)>0:
            for app in apps:
                print(app['name'])

                app['server_name']=server.name
                app['server_ip']=server.ip
                
                webapp_object, created = WebApp.objects.update_or_create(
                    name=app['name'],
                    defaults={"data": app}
                )
    return redirect('webapps_index')

    # webapp_list = WebApp.objects.all()  # .order_by("-pub_date")[:5]
    # context = {"webapp_list": webapp_list}
    #
    # return render(request, "apps/index.html", context)
