from django.shortcuts import render
from .models import WebApp
from subprocess import run,check_output

from servers.models import Server
import paramiko
import json
def index(request):
    webapp_list = WebApp.objects.all()  # .order_by("-pub_date")[:5]
    context = {"webapp_list": webapp_list}
    return render(request, "apps/index.html", context)

def connect_and_find_apps(ip):

	command = 'scp -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null scripts/find_apps.py root@{}:~/'.format(
		ip)
	output = check_output(command, shell=True)
	print(output.decode())


	paramikoclient = paramiko.SSHClient()
	paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoclient.connect(ip, username='root')
	ssh_stdin, ssh_stdout, ssh_stderr = paramikoclient.exec_command("python3 find_apps.py")
	exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
	# print(ssh_stdout.read().decode())#.replace('\n', ' '))
	json_out=ssh_stdout.read().decode().splitlines()
	print(json_out)
	if len(json_out)>=1:
		json_out=json_out[-1].strip()
		# print(json_out)
		json_acceptable_string = json_out.replace("'", "\"")
		json_object = json.loads(json_acceptable_string)
	else:
		json_object={}
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
		apps=connect_and_find_apps(server.ip)
		print('apps',apps)
		if len(apps)>0:
			for app_name in apps:
				print(app_name,apps[app_name])
				webapp_object, created = WebApp.objects.update_or_create(
					name=app_name,
					defaults={"data": apps[app_name]}
				)

	webapp_list = WebApp.objects.all()  # .order_by("-pub_date")[:5]
	context = {"webapp_list": webapp_list}

	return render(request, "apps/index.html", context)
