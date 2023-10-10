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

        #try to connect
        paramikoclient = paramiko.SSHClient()
        paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # paramikoclient.load_system_host_keys()
        try:
            paramikoclient.connect(ip, username='root')
            ssh_stdin, ssh_stdout, ssh_stderr = paramikoclient.exec_command("ls -alrt")
            exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
            print('paramiko can connect', exit_code)
            status='paramiko can connect'
        except paramiko.ssh_exception.AuthenticationException:
            status='paramiko cant connect'



        server_object, created = Server.objects.update_or_create(
            name=server.name,
            defaults={"ip": ip,"status":status}
        )
        # server_object.save()
        # visitor, created = Visitor.objects.update_or_create(
        #     name="Harry", surname="Potter", defaults={"age": 21}
        # )

    server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    context = {"server_list": server_list}
    return render(request, "servers/index.html", context)

def add_sshkey_to_servers(request):
    #get all servers and try to connect, if it doesn't work try to add pub keys:
    print('Add Key to servers!')

    hetznerkey = CloudKey.objects.get(cloudprovider="Hetzner")
    sshkey = SSHKey.objects.first()

    client = Client(token=hetznerkey.key)  # Please paste your API token here
    #
    # List your servers
    # servers = client.servers.get_all()
    # server=client.servers.get_by_name(server_name)

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
        # print(ssh_key.public_key)

    # get ssh key name
    home = expanduser("~")
    localsshkey = open('{}/.ssh/id_rsa.pub'.format(home), 'r').readlines()[0]
    localsshkeyname = localsshkey.strip().split()[2]
    # print(localsshkeyname,localsshkey)
    if localsshkeyname not in ssh_keys_dict:
        # create ssh key on hetzner
        sshkeyresponse = client.ssh_keys.create(name=localsshkeyname, public_key=localsshkey)
        ssh_keys_dict[sshkeyresponse.name] = {}
        ssh_keys_dict[sshkeyresponse.name]['id'] = sshkeyresponse.id
        ssh_keys_dict[sshkeyresponse.name]['public_key'] = sshkeyresponse.public_key

    for server in servers:
        ip = server.public_net.ipv4.ip
        print(f"{server.id=} {server.name=} {server.status=} {ip=}")

        # newpass=server.reset_password()
        # print(newpass.root_password,ip)
        # break
        # rescue mode
        response = server.enable_rescue(type='linux64', ssh_keys=[ssh_keys_dict[localsshkeyname]['id']])  # ,
        # rootpass= response.root_password
        # print(rootpass)
        # time.sleep(30)
        response.action.wait_until_finished()
        rebootresponse = server.reboot()

        print(rebootresponse.wait_until_finished())

        time.sleep(30)

        print('connect with ssh')
        paramikoclient = paramiko.SSHClient()
        paramikoclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # paramikoclient.load_system_host_keys()
        # paramikoclient.connect(ip, username='root', password = rootpass)
        # stdin, stdout, stderr = paramikoclient.exec_command('ls -l')

        # ssh_stdin, ssh_stdout, ssh_stderr = paramikoclient.exec_command("ls -alrt")
        # exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
        #
        # for line in ssh_stdout:
        #     print(line.strip())

        command = 'ssh -o StrictHostKeyChecking=no root@{} mkdir /mnt/hd'.format(ip)
        output = check_output(command, shell=True)
        print(output.decode())

        command = 'ssh -o StrictHostKeyChecking=no root@{} mkdir /mnt/hd'.format(ip)
        output = check_output(command, shell=True)
        print(output.decode())

        command = 'ssh -o StrictHostKeyChecking=no root@{} ls'.format(ip)
        output = check_output(command, shell=True)
        print(output.decode())

        # connect to server
        # add ssh key
        # reboot
        # try to connect

        break

        # echo "keyfile_content" >> / root /.ssh / authorized_keys

        # print(server.public_net.ipv4_address)
        # print(server.public_net)
        # print(server.public_net.ipv4)
        # print(server.public_net.ipv4.ip)

        # get private ssh key and try to connect to the server
        
        server_object = Server(
            name=server.name,
            ip=ip)
        server_object.save()
        # visitor, created = Visitor.objects.update_or_create(
        #     name="Harry", surname="Potter", defaults={"age": 21}
        # )

    server_list = Server.objects.all()  # .order_by("-pub_date")[:5]
    context = {"server_list": server_list}
    return render(request, "servers/index.html", context)