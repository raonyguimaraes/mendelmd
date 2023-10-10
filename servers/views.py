from django.shortcuts import render
from subprocess import run,check_output
# hvloud reqs
from hcloud import Client

from keys.models import CloudKey, SSHKey
from .models import Server
import time
from os.path import expanduser
import paramiko

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
    server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    context = {"server_list": server_list}
    return render(request, "servers/index.html", context)

def try_to_connect(ip):
    #try to connect
    paramikoclient = paramiko.SSHClient()
    paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # paramikoclient.load_system_host_keys()
    try:
        paramikoclient.connect(ip, username='root')
        ssh_stdin, ssh_stdout, ssh_stderr = paramikoclient.exec_command("ls -alrt")
        exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
        print('paramiko can connect', exit_code)
        status=0
    except paramiko.ssh_exception.AuthenticationException:
        status=1
    return(status)

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

        status=try_to_connect(ip)

        server_object, created = Server.objects.update_or_create(
            name=server.name,
            defaults={"ip": ip,"status":status}
        )
        

    server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    context = {"server_list": server_list}
    return render(request, "servers/index.html", context)

def add_local_ssh_key_to_hetzner(client):
    # get ssh key name
    home = expanduser("~")
    local_ssh_key = open('{}/.ssh/id_rsa.pub'.format(home), 'r').readlines()[0]
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
    

def add_sshkey_to_servers(request):
    #get all servers and try to connect, if it doesn't work try to add pub keys:
    print('Add Key to servers!')

    hetznerkey = CloudKey.objects.get(cloudprovider="Hetzner")
    client = Client(token=hetznerkey.key)  # Please paste your API token here
    
    #add local ssh key to hetzner

    ssh_key_hetzner_id=add_local_ssh_key_to_hetzner(client)
    print('ssh_key_hetzner_id', ssh_key_hetzner_id)

    servers = client.servers.get_all()

    for server in servers:
        ip = server.public_net.ipv4.ip
        print(f"{server.id=} {server.name=} {server.status=} {ip=}")

        status=try_to_connect(ip)

        if status==1:
            print('Try to add ssh key')
            response = server.enable_rescue(type='linux64', ssh_keys=[ssh_key_hetzner_id]) 
            response.action.wait_until_finished() 
            rebootresponse = server.reboot()
            rebootresponse.wait_until_finished()
            time.sleep(45)
            
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

            rebootresponse = server.reboot()
            rebootresponse.wait_until_finished()
            time.sleep(45)

            status=try_to_connect(ip)
            print('Now it can connect!')
        else:
            print('Can already connect! Great.')
        server_object, created = Server.objects.update_or_create(
            name=server.name,
            defaults={"ip": ip,"status":status}
        )

    server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    context = {"server_list": server_list}
    return render(request, "servers/index.html", context)

def update_usage(request):

    servers = Server.objects.all()
    for server in servers:
        print(server.name,server.ip)

        paramikoclient = paramiko.SSHClient()
        paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramikoclient.connect(server.ip, username='root')
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