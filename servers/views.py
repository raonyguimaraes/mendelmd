import socket
import subprocess
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

# relative import of forms
from .models import Server
from .forms import ServerForm

from django.shortcuts import render
from subprocess import run,check_output
# hvloud reqs
from hcloud import Client
from time import sleep

from paramiko.ssh_exception import BadHostKeyException, AuthenticationException, SSHException, NoValidConnectionsError

from keys.models import CloudKey, SSHKey
import time
from os.path import expanduser
import paramiko
import os


# ['STATUS_DELETING', 'STATUS_INIT', 'STATUS_MIGRATING',
# 'STATUS_OFF', 'STATUS_REBUILDING', 'STATUS_RUNNING',
# 'STATUS_STARTING', 'STATUS_STOPPING', 'STATUS_UNKNOWN',
# '__annotations__', '__class__', '__delattr__', '__dict__',
# '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__',
# '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
# '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__',
# '__subclasshook__', '__weakref__', '_client', 'add_to_placement_group', 'attach_iso', 'attach_to_network',
# 'backup_window', 'change_alias_ips', 'change_dns_ptr', 'change_protection', 'change_type',
# 'complete', 'create_image', 'created', 'data_model', 'datacenter', 'delete', 'detach_from_network',
# 'detach_iso', 'disable_backup', 'disable_rescue', 'enable_backup', 'enable_rescue', 'from_dict', 'get_actions',
# 'get_actions_list', 'id', 'image', 'included_traffic', 'ingoing_traffic', 'iso', 'labels', 'locked', 'model', 'name',
# 'outgoing_traffic', 'placement_group', 'power_off', 'power_on', 'primary_disk_size', 'private_net', 'protection', 'public_net',
# 'reboot', 'rebuild', 'reload', 'remove_from_placement_group', 'request_console', 'rescue_enabled', 'reset', 'reset_password',
# 'server_type', 'shutdown', 'status', 'update', 'volumes']
#https://community.hetzner.com/tutorials/howto-ssh-key

def index(request):
    server_list = Server.objects.all().order_by("id")  # .order_by("-pub_date")[:5]
    server_count=server_list.count()
    total_cost = server_list.aggregate(total_price=Sum('cost'))
    context = {
        "server_list": server_list,
        "total_cost": total_cost,
        "server_count":server_count
    }

    return render(request, "servers/index.html", context)

def create(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = ServerForm(request.POST or None)
    if form.is_valid():

        # if form.cleaned_data['url']!='':
        #     print('get ip')
        #     form.cleaned_data['ip']=socket.gethostbyname(form.cleaned_data['url'])
        #     print(form.cleaned_data)
        form.save()
        return redirect('servers_index')

    context['form'] = form
    return render(request, "servers/create_view.html", context)


# delete view for details
def delete_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}
    # fetch the object related to passed id
    obj = get_object_or_404(Server, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect('servers_index')

    return render(request, "servers/delete_view.html", context)

def terminate_view(request,id):
    # dictionary for initial data with
    # field names as keys
    context = {}
    # fetch the object related to passed id
    obj = get_object_or_404(Server, id=id)

    if request.method == "POST":
        hetznerkey = CloudKey.objects.get(cloudprovider="Hetzner")
        client = Client(token=hetznerkey.key)  # Please paste your API token here
        servers = client.servers.get_all()
        for server in servers:
            ip = server.public_net.ipv4.ip
            if server.name == obj.name and ip == obj.ip:
                print('DELETE NOW')
                server.delete()
                obj.status='terminated'
                obj.save()
                # response = server.enable_rescue(type='linux64', ssh_keys=[ssh_key_hetzner_id])
                # response.action.wait_until_finished()
                # rebootresponse = server.reboot()
                # rebootresponse.wait_until_finished()
            # print(f"{server.id=} {server.name=} {server.status=} {ip=}")


        # delete object
        # obj.delete()
        # after deleting redirect to
        # home page
        return redirect('servers_index')

    return render(request, "servers/terminate_view.html", context)

# pass id attribute from urls
def detail_view(request, id):
    # dictionary for initial data with
    # field names as keys
    # context = {}

    # add the dictionary during initialization
    # context["data"] = Server.objects.get(id=id)
    server=Server.objects.get(id=id)
    if server.password:
        server.password = '****'
    context = {"server": server}

    return render(request, "servers/detail_view.html", context)


# update view for details
def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Server, id=id)

    # pass the object as instance in form
    form = ServerForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect('servers_index')

    # add form dictionary to context
    context["form"] = form

    return render(request, "servers/update_view.html", context)

# def try_to_connect(ip):

#     #check if it doesn exists
#     home = expanduser("~")
#     key_path='{}/.ssh/id_rsa'.format(home)
    
#     if not os.path.isfile(key_path):
#         print('create key')
#         # command = 'ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y >/dev/null 2>&1'
#         command="""ssh-keygen -b 2048 -t rsa -f {} -q -N "" """.format(key_path)
#         run(command,shell=True)


#     #try to connect
#     paramikoclient = paramiko.SSHClient()
#     paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     paramikoclient.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
#     paramikoclient.load_system_host_keys()

#     try:
#         paramikoclient.connect(ip, username='root')
#         ssh_stdin, ssh_stdout, ssh_stderr = paramikoclient.exec_command("ls -alrt")
#         exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
#         print('paramiko can connect', exit_code)
#         status=0
#     except paramiko.ssh_exception.AuthenticationException:
#         status=1
#     return(status)


def check_status(request):
    print('Import Servers!')
    hetznerkey = CloudKey.objects.get(cloudprovider="Hetzner")
    sshkey = SSHKey.objects.first()

    servers = Server.objects.all()
    # Server.objects.all().delete()

    for server in servers:
        ip = server.ip
        print(f"{server.id=} {server.name=} {server.status=} {ip=}")

        # status = try_to_connect(ip)
        status=check_ssh(ip, username=server.username, password=server.password)

        server_object, created = Server.objects.update_or_create(
            name=server.name,
            defaults={"status": status}
        )

    return redirect('servers_index')

    # server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    # context = {"server_list": server_list}
    # return render(request, "servers/index.html", context)

def check_ssh(ip, username, password, key_file=None, initial_wait=2, interval=5, retries=1):

    if key_file==None:
        key_file=expanduser("~/.ssh/id_rsa.pub")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
    # ssh.load_system_host_keys()

    sleep(initial_wait)
    # knownhosts = expanduser("~/.ssh/known_hosts")
    
    # command = 'ssh-keygen -f "{}" -R {}'.format(knownhosts, ip)
    # check_output(command,shell=True)
    
    # knownhosts = expanduser("~/.ssh/known_hosts")
    # command = 'ssh-keyscan -T 240 {} >> {}'.format(ip,knownhosts)
    # # check_output(command,shell=True)
    
    # try:
    #     subprocess.check_output(command, shell=True)
    # except subprocess.CalledProcessError as e:
    #     print(e.returncode)
    #     print(e.output)
    

    for x in range(retries):
        try:
            ssh.connect(ip, username=username, password=password, key_filename=key_file, banner_timeout=200)
            return True
        except (BadHostKeyException, AuthenticationException,
                SSHException, socket.error, NoValidConnectionsError) as e:
            print(e)
            sleep(interval)
    return False

def import_from_hetzner(request):

    print('Import Servers!')
    hetznerkey = CloudKey.objects.get(cloudprovider="Hetzner")
    sshkey = SSHKey.objects.first()

    client = Client(token=hetznerkey.key)  # Please paste your API token here

    # print(sshkey)

    # List your servers
    servers = client.servers.get_all()
    # Server.objects.all().delete()


    for server in servers:
        ip = server.public_net.ipv4.ip
        print(f"{server.id=} {server.name=} {server.status=} {ip=}")

        # status=try_to_connect(ip)
        
        knownhosts = expanduser("~/.ssh/known_hosts")
        command = f'ssh-keyscan -T 240 {ip} >> {knownhosts}'#.format(ip,knownhosts)
        check_output(command,shell=True)
        
        key_file=expanduser("~/.ssh/id_rsa.pub")
        status=check_ssh(ip, 'root', None, key_file)

        server_object, created = Server.objects.update_or_create(
            name=server.name,
            username='root',
            provider='hetzner_cloud',
            defaults={"ip": ip,"status":status}
        )
        
    return redirect('servers_index')

    # server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    # context = {"server_list": server_list}
    # return render(request, "servers/index.html", context)

def add_local_ssh_key_to_hetzner(client):
    # get ssh key name
    home = expanduser("~")
    key_path='{}/.ssh/id_rsa.pub'.format(home)
    local_ssh_key = open(key_path, 'r').readlines()[0]
    local_ssh_key_name = local_ssh_key.strip().split()[2]
    
    servers = client.servers.get_all()
    ssh_keys = client.ssh_keys.get_all()
    ssh_keys_dict = {}
    # print(ssh_keys)
    ssh_key_names = []
    for ssh_key in ssh_keys:
        # print(ssh_key.name,ssh_key.id)
        # ssh_key_names.append(ssh_key.name)
        ssh_keys_dict[ssh_key.name] = {}
        ssh_keys_dict[ssh_key.name]['id'] = ssh_key.id
        ssh_keys_dict[ssh_key.name]['public_key'] = ssh_key.public_key
    if local_ssh_key_name not in ssh_keys_dict:
        # create ssh key on hetzner
        sshkeyresponse = client.ssh_keys.create(name=local_ssh_key_name, public_key=local_ssh_key)
        ssh_keys_dict[sshkeyresponse.name] = {}
        ssh_keys_dict[sshkeyresponse.name]['id'] = sshkeyresponse.id
        ssh_keys_dict[sshkeyresponse.name]['public_key'] = sshkeyresponse.public_key

    ssh_key_hetzner_id=ssh_keys_dict[local_ssh_key_name]['id']
    return(ssh_key_hetzner_id)
    

def add_sshkey_to_server(request, id):
    
    obj=Server.objects.get(id=id)
    print('Add Key to server')
    
    hetznerkey = CloudKey.objects.get(cloudprovider="Hetzner")
    client = Client(token=hetznerkey.key)  # Please paste your API token here
    
    home = expanduser("~")
    key_path = '{}/.ssh/id_rsa.pub'.format(home)

    #add local ssh key to hetzner
    ssh_key_hetzner_id=add_local_ssh_key_to_hetzner(client)
    print('ssh_key_hetzner_id', ssh_key_hetzner_id)
    
    server = client.servers.get_by_name(name=obj.name) # .get_all()
    
    ip = server.public_net.ipv4.ip
    
    print('Try to add ssh key')
    response = server.enable_rescue(type='linux64', ssh_keys=[ssh_key_hetzner_id])
    response.action.wait_until_finished()
    rebootresponse = server.reboot()
    rebootresponse.wait_until_finished()
    # time.sleep(120)
    print('after reboot, now try to ssh')
    status=check_ssh(ip, obj.username, obj.password, key_path, initial_wait=3, interval=10, retries=20)
    print('after check ssh suceeds')
    
    # print(server)
    # # for server in servers:
    # ip = server.public_net.ipv4.ip
    # print(ip)
    
    
    context = {"server": obj}
    return render(request, "servers/detail_view.html", context)
    

def add_sshkey_to_servers(request):
    #get all servers and try to connect, if it doesn't work try to add pub keys:
    print('Add Key to servers!')

    hetznerkey = CloudKey.objects.get(cloudprovider="Hetzner")
    client = Client(token=hetznerkey.key)  # Please paste your API token here
    home = expanduser("~")
    key_path = '{}/.ssh/id_rsa.pub'.format(home)

    #add local ssh key to hetzner

    ssh_key_hetzner_id=add_local_ssh_key_to_hetzner(client)
    print('ssh_key_hetzner_id', ssh_key_hetzner_id)

    servers = client.servers.get_all()

    for server in servers:

        ip = server.public_net.ipv4.ip
        server_obj = Server.objects.get(ip=ip)

        print(f"{server.id=} {server.name=} {server.status=} {ip=}")
        print('server_obj',server_obj,server_obj.provider)

        status=check_ssh(ip, server_obj.username, server_obj.password)


        if status==False:
            
            print('Try to add ssh key')
            response = server.enable_rescue(type='linux64', ssh_keys=[ssh_key_hetzner_id])
            response.action.wait_until_finished()
            rebootresponse = server.reboot()
            rebootresponse.wait_until_finished()
            # time.sleep(120)
            print('after reboot, now try to ssh')
            status=check_ssh(ip, server_obj.username, server_obj.password, key_path, initial_wait=3, interval=10, retries=20)
            print('after check ssh suceeds')
            
            # paramikoclient = paramiko.SSHClient()
            # paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # paramikoclient.connect(ip, username='root')
            # ssh_stdin, ssh_stdout, ssh_stderr = paramikoclient.exec_command("ls -alrt")
            # exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
            # for line in ssh_stdout:
            #     print(line.strip())
            # break

            command = 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null scripts/add_ssh_key.py root@{}:~/'.format(ip)
            output = check_output(command, shell=True)
            print(output.decode())

            command = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@{} python3 add_ssh_key.py'.format(ip)
            output = check_output(command, shell=True)
            print(output.decode())
            
            print('nwo reboot again after adding the key')

            rebootresponse = server.reboot()
            rebootresponse.wait_until_finished()
            # time.sleep(120)
            status=check_ssh(ip, server_obj.username, server_obj.password, key_path, initial_wait=3, interval=10, retries=20)

            # status=try_to_connect(ip)

            print('Now it can connect!')
        else:
            print('Can already connect! Great.')

        server_object, created = Server.objects.update_or_create(
            name=server.name,
            defaults={"ip": ip,"status":status}
        )
    #now deal with non hetzner server
    servers = Server.objects.all().exclude(provider='hetzner_cloud')
    for server in servers:
        print('install keys')
        key = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server.ip, username=server.username, password=server.password, banner_timeout=200)
        client.exec_command('mkdir -p ~/.ssh/')
        client.exec_command('echo "%s" > ~/.ssh/authorized_keys' % key)
        client.exec_command('chmod 644 ~/.ssh/authorized_keys')
        client.exec_command('chmod 700 ~/.ssh/')
        status=check_ssh(server.ip, server.username, server.password,retries=2)
        ip=server.ip
        server_object, created = Server.objects.update_or_create(
            name=server.name,
            defaults={"ip": ip,"status":status}
        )

    return redirect('servers_index')

    # server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    # context = {"server_list": server_list}
    # return render(request, "servers/index.html", context)

def update_usage(request):

    servers = Server.objects.all()
    for server in servers:
        print(server.name,server.ip)

        paramikoclient = paramiko.SSHClient()
        paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        paramikoclient.connect(server.ip, username=server.username,password=server.password, banner_timeout=200)

        subcomand = '''echo "Load  `LC_ALL=C top -bn1 | head -n 1` , `LC_ALL=C top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}'`% RAM `free -m | awk '/Mem:/ { printf("%3.1f%%", $3/$2*100) }'` HDD `df -h / | awk '/\// {print $(NF-1)}'`"'''
        ssh_stdin, ssh_stdout, ssh_stderr = paramikoclient.exec_command(subcomand)
        # exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
        # for line in ssh_stdout:
        #     print(line.strip())
        # print()
        server.usage = ssh_stdout.readlines()[0].strip()
        print(server.usage)
        server.save()    

        # command = """ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@{} {}""".format(server.ip,subcomand)
        # print(command)
        # output = check_output(command, shell=True)
        # print(output.decode())
        # break

    server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    context = {"server_list": server_list}
    return render(request, "servers/index.html", context)


def reboot(request):

    servers = Server.objects.all()
    for server in servers:
        print(server.name,server.ip)

        paramikoclient = paramiko.SSHClient()
        paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            paramikoclient.connect(server.ip, username='root', banner_timeout=200)
            subcomand = '''reboot'''
            ssh_stdin, ssh_stdout, ssh_stderr = paramikoclient.exec_command(subcomand)
        except e:
            print(e)
            pass

    server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    context = {"server_list": server_list}
    return render(request, "servers/index.html", context)

@login_required
def servers_bulk_action(request):
    if request.method == 'POST':
        servers = request.POST.getlist('servers')
        print(servers) 
        servers = list(reversed([int(x) for x in servers]))
        print(servers)
        
        # if request.POST['selectionField'] == "Show":
        #     for individual_id in individuals:
        #         individual = get_object_or_404(Individual, pk=individual_id)
        #         individual.featured = True
        #         individual.save()
        # if request.POST['selectionField'] == "Hide":
        #     for individual_id in individuals:
        #         individual = get_object_or_404(Individual, pk=individual_id)
        #         individual.featured = False
        #         individual.save()
        if request.POST['selectionField'] == "Delete":
            for server_id in servers:
                server = get_object_or_404(Server, pk=server_id)
                server.delete()
        #         individual_id = individual.id
        #         if individual.user:
        #             username = individual.user.username
        #         else:
        #             username = 'public'
        #         #delete files
        #         if individual.vcf_file:
        #             individual.vcf_file.delete()
        #         # if individual.strs_file:
        #         #     individual.strs_file.delete()
        #         # if individual.cnvs_file:
        #         #     individual.cnvs_file.delete()
        #         os.system('rm -rf %s/genomes/%s/%s' % (settings.BASE_DIR, slugify(username), individual_id))

        #         individual.delete()
        #     messages.add_message(request, messages.INFO, "Individuals deleted with success!")
        #     #os.system('rm -rf rockbio14/site_media/media/genomes/%s/%s' % (username, individual_id))
        # if request.POST['selectionField'] == "Populate":
        #     for individual_id in individuals:
        #         individual = get_object_or_404(Individual, pk=individual_id)
        #         PopulateVariants.delay(individual.id)
            
        # if request.POST['selectionField'] == "Annotate":
        #     for individual_id in individuals:
        #         individual = get_object_or_404(Individual, pk=individual_id)
        #         individual.status = 'new'
        #         individual.n_lines = 0
        #         individual.save()
        #         AnnotateVariants.delay(individual.id)
        # if request.POST['selectionField'] == "Find_Medical_Conditions_and_Medicines":
        #     for individual_id in individuals:
        #         individual = get_object_or_404(Individual, pk=individual_id)
        #         Find_Medical_Conditions_and_Medicines.delay(individual.id)
    
    return redirect('servers_index')
